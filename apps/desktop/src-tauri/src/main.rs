use std::fs::{create_dir_all, OpenOptions};
use std::io::{Read, Write};
use std::net::TcpStream;
use std::path::PathBuf;
use std::process::{Child, Command, Stdio};
use std::sync::Mutex;
use std::time::{Duration, SystemTime, UNIX_EPOCH};

use tauri::{path::BaseDirectory, Manager};

struct ApiSidecar(Mutex<Option<Child>>);

impl Drop for ApiSidecar {
    fn drop(&mut self) {
        if let Ok(mut child) = self.0.lock() {
            if let Some(mut child) = child.take() {
                let _ = child.kill();
            }
        }
    }
}

fn log_path() -> PathBuf {
    if let Ok(appdata) = std::env::var("APPDATA") {
        return PathBuf::from(appdata)
            .join("MyNotes AI")
            .join("logs")
            .join("desktop.log");
    }

    std::env::temp_dir()
        .join("MyNotes AI")
        .join("logs")
        .join("desktop.log")
}

fn timestamp() -> String {
    match SystemTime::now().duration_since(UNIX_EPOCH) {
        Ok(duration) => format!("{}", duration.as_secs()),
        Err(_) => "unknown-time".to_string(),
    }
}

fn write_log(path: &PathBuf, message: impl AsRef<str>) {
    if let Some(parent) = path.parent() {
        let _ = create_dir_all(parent);
    }

    if let Ok(mut file) = OpenOptions::new().create(true).append(true).open(path) {
        let _ = writeln!(file, "[{}] {}", timestamp(), message.as_ref());
    }
}

#[cfg(windows)]
fn show_error(title: &str, message: &str) {
    use std::iter::once;
    use std::os::windows::ffi::OsStrExt;
    use windows_sys::Win32::UI::WindowsAndMessaging::{MessageBoxW, MB_ICONERROR, MB_OK};

    let title_wide: Vec<u16> = std::ffi::OsStr::new(title)
        .encode_wide()
        .chain(once(0))
        .collect();
    let message_wide: Vec<u16> = std::ffi::OsStr::new(message)
        .encode_wide()
        .chain(once(0))
        .collect();

    unsafe {
        MessageBoxW(
            std::ptr::null_mut(),
            message_wide.as_ptr(),
            title_wide.as_ptr(),
            MB_OK | MB_ICONERROR,
        );
    }
}

#[cfg(not(windows))]
fn show_error(title: &str, message: &str) {
    eprintln!("{title}: {message}");
}

fn check_api_health(port: &str) -> Result<String, String> {
    let address = format!("127.0.0.1:{port}");
    let mut stream = TcpStream::connect(address.as_str()).map_err(|err| err.to_string())?;
    stream
        .set_read_timeout(Some(Duration::from_secs(2)))
        .map_err(|err| err.to_string())?;
    stream
        .set_write_timeout(Some(Duration::from_secs(2)))
        .map_err(|err| err.to_string())?;

    let request =
        format!("GET /api/health HTTP/1.1\r\nHost: 127.0.0.1:{port}\r\nConnection: close\r\n\r\n");
    stream
        .write_all(request.as_bytes())
        .map_err(|err| err.to_string())?;

    let mut response = String::new();
    stream
        .read_to_string(&mut response)
        .map_err(|err| err.to_string())?;

    if response.contains("\"status\":\"ok\"") || response.contains("\"status\": \"ok\"") {
        Ok(response.lines().next().unwrap_or("health ok").to_string())
    } else {
        Err(response
            .lines()
            .next()
            .unwrap_or("empty health response")
            .to_string())
    }
}

fn poll_api_health(port: String, log_path: PathBuf) {
    std::thread::spawn(move || {
        for attempt in 1..=30 {
            match check_api_health(&port) {
                Ok(summary) => {
                    write_log(
                        &log_path,
                        format!(
                            "/api/health check result: success on attempt {attempt}: {summary}"
                        ),
                    );
                    return;
                }
                Err(err) => {
                    write_log(
                        &log_path,
                        format!("/api/health check result: attempt {attempt} failed: {err}"),
                    );
                    std::thread::sleep(Duration::from_secs(1));
                }
            }
        }

        let message = format!(
            "MyNotes AI 后端启动失败。可能原因：8000 端口被占用，或安装包不完整。请重启电脑后重试，或查看日志：{}",
            log_path.display()
        );
        write_log(&log_path, "sidecar health check failed after 30 seconds");
        show_error("MyNotes AI", &message);
    });
}

fn pipe_sidecar_output(
    log_path: PathBuf,
    label: &'static str,
    pipe: Option<impl Read + Send + 'static>,
) {
    if let Some(mut pipe) = pipe {
        std::thread::spawn(move || {
            let mut buffer = [0_u8; 1024];
            loop {
                match pipe.read(&mut buffer) {
                    Ok(0) => return,
                    Ok(size) => {
                        let text = String::from_utf8_lossy(&buffer[..size]);
                        write_log(&log_path, format!("mynotes-api {label}: {}", text.trim()));
                    }
                    Err(err) => {
                        write_log(&log_path, format!("mynotes-api {label} read error: {err}"));
                        return;
                    }
                }
            }
        });
    }
}

fn main() {
    let startup_log_path = log_path();
    write_log(&startup_log_path, "app start time");

    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .setup(|app| {
            let log_path = log_path();
            write_log(&log_path, "setup started");

            match app.path().resource_dir() {
                Ok(resource_dir) => {
                    write_log(
                        &log_path,
                        format!("frontendDist/resource path: {}", resource_dir.display()),
                    );
                }
                Err(err) => {
                    let message = format!(
                        "MyNotes AI 前端资源加载失败。安装包可能不完整，缺少 index.html。请重新安装最新 MSI。\n\n日志：{}",
                        log_path.display()
                    );
                    write_log(&log_path, format!("frontendDist path error: {err}"));
                    show_error("MyNotes AI", &message);
                    return Err(Box::new(err));
                }
            }

            match app.path().resolve("resources/index.html", BaseDirectory::Resource) {
                Ok(index_path) => {
                    write_log(
                        &log_path,
                        format!(
                            "index.html existence check result: {} ({})",
                            index_path.exists(),
                            index_path.display()
                        ),
                    );
                }
                Err(err) => {
                    write_log(&log_path, format!("index.html resolve check failed: {err}"));
                }
            }

            if std::env::var("MYNOTES_SKIP_SIDECAR").is_ok() {
                write_log(
                    &log_path,
                    "MYNOTES_SKIP_SIDECAR is set; sidecar startup skipped for development",
                );
                return Ok(());
            }

            let port = std::env::var("MYNOTES_API_PORT").unwrap_or_else(|_| "8000".to_string());
            write_log(&log_path, format!("MYNOTES_API_PORT={port}"));

            let sidecar_path = match app
                .path()
                .resolve("resources/binaries/mynotes-api.exe", BaseDirectory::Resource)
            {
                Ok(path) => {
                    write_log(
                        &log_path,
                        format!(
                            "sidecar expected path: {} exists={}",
                            path.display(),
                            path.exists()
                        ),
                    );
                    path
                }
                Err(err) => {
                    let message = format!(
                        "MyNotes AI 后端启动失败。安装包不完整，缺少 resources\\binaries\\mynotes-api.exe。请重新安装最新 MSI，或查看日志：{}",
                        log_path.display()
                    );
                    write_log(&log_path, format!("sidecar expected path resolve failed: {err}"));
                    show_error("MyNotes AI", &message);
                    return Err(Box::new(err));
                }
            };

            if !sidecar_path.exists() {
                let message = format!(
                    "MyNotes AI 后端启动失败。安装包不完整，缺少 resources\\binaries\\mynotes-api.exe。请重新安装最新 MSI，或查看日志：{}",
                    log_path.display()
                );
                write_log(
                    &log_path,
                    format!("sidecar missing at {}", sidecar_path.display()),
                );
                show_error("MyNotes AI", &message);
                return Err(std::io::Error::new(std::io::ErrorKind::NotFound, message).into());
            }

            let mut sidecar = Command::new(&sidecar_path);
            sidecar
                .env("MYNOTES_ENV", "desktop")
                .env("MYNOTES_API_PORT", port.clone())
                .stdout(Stdio::piped())
                .stderr(Stdio::piped());

            #[cfg(windows)]
            {
                use std::os::windows::process::CommandExt;
                sidecar.creation_flags(0x08000000);
            }

            let mut child = match sidecar.spawn() {
                Ok(result) => result,
                Err(err) => {
                    let message = format!(
                        "MyNotes AI 后端启动失败。可能原因：8000 端口被占用，或安装包不完整。请重启电脑后重试，或查看日志：{}",
                        log_path.display()
                    );
                    write_log(&log_path, format!("sidecar start failure: {err}"));
                    show_error("MyNotes AI", &message);
                    return Err(Box::new(err));
                }
            };

            write_log(&log_path, "sidecar start success");
            pipe_sidecar_output(log_path.clone(), "stdout", child.stdout.take());
            pipe_sidecar_output(log_path.clone(), "stderr", child.stderr.take());
            app.manage(ApiSidecar(Mutex::new(Some(child))));

            poll_api_health(port, log_path);

            Ok(())
        })
        .run(tauri::generate_context!())
        .unwrap_or_else(|err| {
            let message = format!(
                "MyNotes AI 启动失败。请查看日志：{}\n\n错误：{}",
                startup_log_path.display(),
                err
            );
            write_log(&startup_log_path, format!("app runtime error: {err}"));
            show_error("MyNotes AI", &message);
        });
}
