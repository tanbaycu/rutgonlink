# TanBayCu - URL Shortener & QR Code Generator

![TanBayCu Logo](https://i.postimg.cc/W3N38R5W/Thi-t-k-ch-a-c-t-n-16.png)

## Giới thiệu

TanBayCu là một công cụ trực tuyến miễn phí giúp bạn rút gọn URL và tạo mã QR. Đơn giản, nhanh chóng và đáng tin cậy.

## Tính năng

- **Rút gọn URL**: Chuyển đổi các URL dài thành các URL ngắn gọn và dễ nhớ.
- **Tạo mã QR**: Tạo mã QR tùy chỉnh với nội dung, màu sắc và kích thước bạn chọn.
- **Giao diện người dùng hiện đại**: Sử dụng Tailwind CSS và Lucide Icons để tạo giao diện người dùng đẹp mắt và dễ sử dụng.
- **Hỗ trợ đa nền tảng**: Chạy trên mọi hệ điều hành và trình duyệt hiện đại.

## Cài đặt

### Yêu cầu

- Python 3.x
- Flask
- requests
- qrcode
- Pillow

### Hướng dẫn cài đặt

1. Clone repo này về máy của bạn:
    ```sh
    git clone https://github.com/tanbaycu/url-shortener-qr-generator.git
    cd url-shortener-qr-generator
    ```

2. Cài đặt các gói phụ thuộc:
    ```sh
    pip install -r requirements.txt
    ```

3. Chạy ứng dụng:
    ```sh
    python app.py
    ```

4. Mở trình duyệt và truy cập `http://localhost:5000` để sử dụng ứng dụng.

## Cấu trúc thư mục

```plaintext
.
├── app.py
├── index.html
├── README.md
├── requirements.txt
├── templates/
│   ├── 404.html
│   └── test.html
└── vercel.json
```
