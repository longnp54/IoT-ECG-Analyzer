import subprocess
import time
import os
import webbrowser
import requests
import tkinter as tk

# Khai báo biến toàn cục để lưu tiến trình
node_red_process = None
plotly_process = None

def stop_node_red_flows():
    """Gửi yêu cầu HTTP để dừng các luồng của Node-RED."""
    try:
        response = requests.post('http://localhost:1880/flows', json={"command": "stop"})
        if response.status_code == 200:
            print("Node-RED flows stopped successfully.")
            return True
        else:
            print(f"Failed to stop Node-RED flows. Status code: {response.status_code}")
            return False
    except requests.ConnectionError:
        print("Node-RED is not running or not accessible on port 1880.")
        return False
    except requests.RequestException as e:
        print(f"Error stopping Node-RED flows: {e}")
        return False

def start_node_red():
    """Khởi động Node-RED và trả về tiến trình con."""
    print("Starting Node-RED...")
    return subprocess.Popen(["node-red"], shell=True)

def start_plotly():
    """Khởi động ứng dụng Dash Plotly và trả về tiến trình con."""
    print("Starting Dash Plotly...")
    script_path = os.path.join(os.path.dirname(__file__), "plotly_dash.py")
    return subprocess.Popen(["python", script_path], shell=True)

def stop_node_red_process():
    """Dừng Node-RED bằng lệnh taskkill."""
    try:
        print("Stopping Node-RED process...")
        subprocess.run(["taskkill", "/f", "/im", "node.exe"], check=True)
        print("Node-RED process stopped successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to stop Node-RED process: {e}")

def stop_plotly_process():
    """Dừng tiến trình Dash Plotly bằng lệnh taskkill."""
    try:
        print("Stopping Dash Plotly process...")
        subprocess.run(["taskkill", "/f", "/im", "python.exe"], check=True)
        print("Dash Plotly process stopped successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to stop Dash Plotly process: {e}")

def stop_execution():
    """Dừng Node-RED và Dash Plotly."""
    global node_red_process, plotly_process
    print("Stopping the services...")

    if node_red_process:
        node_red_process.terminate()  # Dừng Node-RED
        node_red_process.wait()  # Đợi Node-RED dừng

    if plotly_process:
        plotly_process.terminate()  # Dừng Dash Plotly
        plotly_process.wait()  # Đợi Dash Plotly dừng

    # Dừng tiến trình Node-RED bằng lệnh taskkill
    stop_node_red_process()

    # Dừng tiến trình Dash Plotly bằng lệnh taskkill
    stop_plotly_process()

    print("Stopped Node-RED and Dash Plotly.")

def open_services():
    """Mở các tab trình duyệt cho Node-RED và Dash Plotly."""
    if node_red_process is None or plotly_process is None:
        # Kiểm tra xem các tiến trình đã được khởi động chưa
        update_status("Chương trình thất bại!")
    else:
        # Mở các tab trình duyệt nếu dịch vụ đã được khởi động
        print("Mở tab trình duyệt...")
        webbrowser.open("http://localhost:1880", new=1)  # Mở tab trình duyệt cho Node-RED
        webbrowser.open("http://localhost:8050", new=1)  # Mở tab trình duyệt cho Dash Plotly

        # Cập nhật trạng thái trên giao diện chính
        update_status("Chương trình đang chạy...")

def close_services():
    """Dừng các tiến trình khi ấn nút Thoát."""
    print("Stopping the services...")
    stop_execution()

    # Kết thúc chương trình khi dừng các tiến trình
    root.quit()

def update_status(message):
    """Cập nhật trạng thái trên giao diện chính."""
    status_label.config(text=message)

# Tạo cửa sổ giao diện
root = tk.Tk()
root.title("Control Node-RED and Dash Plotly")

# Thiết lập kích thước cửa sổ
root.geometry("300x200")

# Tạo Label để hiển thị trạng thái
status_label = tk.Label(root, text="Chương trình chưa khởi động.", font=("Arial", 12))
status_label.pack(pady=20)

# Tạo nút "Mở"
open_button = tk.Button(root, text="Mở", bg="green", fg="white", command=open_services, width=20)
open_button.pack(pady=20)

# Tạo nút "Thoát"
exit_button = tk.Button(root, text="Thoát", bg="red", fg="white", command=close_services, width=20)
exit_button.pack(pady=20)

# Khởi động server trước khi giao diện xuất hiện
node_red_process = start_node_red()
time.sleep(5)  # Đợi một chút để Node-RED khởi động hoàn tất

plotly_process = start_plotly()

# Cập nhật trạng thái khi chương trình khởi động xong
update_status("Chương trình đã sẵn sàng!")

# Chạy giao diện
root.mainloop()
