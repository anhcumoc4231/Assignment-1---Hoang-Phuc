# ADY201m — Cardiovascular Disease Assignment

## Trạng thái
- Đã khôi phục và kiểm tra CSV: 70.000 dòng, 13 cột, 34.979 hồ sơ mắc bệnh.
- Đã chạy 13 SELECT bằng SQLite local. Đây không phải kết quả chạy IBM Db2 Cloud.
- Đã chạy toàn bộ phân tích, biểu đồ, kiểm định, OLS, 7 mô hình mẫu, baseline và Gradient Boosting tinh chỉnh.
- Chưa chạy IBM Db2 Cloud/Watson Studio: tài khoản dừng tại bước Finish setting up your account / Upgrade account rồi bị đăng xuất; người dùng chưa nâng cấp gói.
- Đã tải bài lên GitHub: https://github.com/anhcumoc4231/ADY201m-Cardio-Assignment (repository riêng tư).
- Để đáp ứng phần Cloud của đề, cần tài khoản IBM đã kích hoạt hoặc môi trường IBM do trường cung cấp, rồi cập nhật notebook có kết quả chạy Cloud.

## Các file chính
- `01_Db2_SQL_Python.ipynb`: DDL/hướng dẫn Db2, 10 truy vấn API và 3 truy vấn bổ sung, xuất CSV, đóng kết nối. Đã chạy chế độ SQLite.
- `02_Cardio_Analysis_ML.ipynb`: notebook đã chạy với kết quả thật.
- `Bao_cao_ADY201m.html`: báo cáo tiếng Việt, mở trực tiếp bằng Chrome, tự chứa biểu đồ.
- `01_Db2_SQL_Python.html`, `02_Cardio_Analysis_ML.html`: bản notebook xem bằng trình duyệt.
- `data/cardio_train_raw.csv`: CSV gốc, delimiter `;`, tuổi theo ngày.
- `data/CARDIO_TRAIN_export.csv`: bản xuất từ chế độ local, delimiter dấu phẩy, tuổi theo ngày.
- `data/cardio_train_clean.csv`: dữ liệu sau IQR toàn bộ tập cho EDA/thống kê, tuổi theo năm.
- `sql/`: DDL Db2 và các SELECT. `cardio_utils.py`: bộ xử lý IQR học trên tập train.
- `results/`: kiểm định, so sánh mô hình, kết quả CV, dự đoán, ID train/test, phiên bản môi trường và mô hình.

## Chạy local
1. Giải nén gói; mở terminal trong thư mục có hai notebook.
2. Dùng Python 3.12 và cài: `python -m pip install -r requirements.txt`.
3. Mở Jupyter: `python -m notebook` (cài thêm `notebook` nếu cần); hoặc mở `.ipynb` bằng VS Code/Jupyter.
4. Chạy notebook 01 với RUN_DB2 mặc định bằng 0 để kiểm chứng local; chạy notebook 02 để phân tích.
5. Không đưa CSV clean theo năm vào notebook đọc raw; việc này sẽ đổi tuổi hai lần.

## Chạy IBM Db2 thật
1. Tạo/đăng nhập tài khoản IBM Cloud của bạn và chọn dịch vụ Db2 có quyền nạp/truy vấn. Kiểm tra chi phí của gói trước khi tạo dịch vụ.
2. Chạy `sql/01_create_table.sql` trong schema riêng. Dùng công cụ nạp dữ liệu của Db2 để nhập `data/cardio_train_raw.csv`, delimiter `;`, dòng đầu chứa tên cột. Không đổi AGE trong bảng thành năm.
3. Chạy `sql/02_queries.sql` trong console. Kiểm tra tổng dòng 70.000 và CARDIO=1 là 34.979.
4. Cài API nếu chưa có: `python -m pip install ibm_db`.
5. Cung cấp biến môi trường DB2_DATABASE, DB2_HOSTNAME, DB2_PORT, DB2_UID, DB2_PWD từ thông tin kết nối của tài khoản riêng. Bật RUN_DB2=1. Có thể cung cấp DB2_SSL_CERT nếu dịch vụ yêu cầu chứng thư.
6. Chạy notebook 01 từ đầu. Không in DSN/mật khẩu; notebook không lưu thông tin đăng nhập vào output. Query bảng CARDIO_TRAIN trong schema mặc định; nếu dùng schema khác, sửa tên bảng thành SCHEMA.CARDIO_TRAIN.
7. Lưu notebook với kết quả kết nối, các truy vấn, CSV xuất và trạng thái cloud_executed=true. Chụp minh chứng trong tài khoản của bạn nếu giảng viên yêu cầu.
8. Không dùng thông tin đăng nhập mẫu trong PDF. Không commit mật khẩu, certificate chứa private key hoặc access token.

## Watson Studio (tài liệu hiện nay dùng tên watsonx.ai Studio)
1. Đăng nhập IBM, tạo/mở project có môi trường notebook phù hợp; tên menu có thể khác theo phiên bản.
2. Nhập `02_Cardio_Analysis_ML.ipynb` từ file. Nạp CSV gốc và `cardio_utils.py` vào môi trường notebook.
3. Đảm bảo `cardio_train_raw.csv` có ở thư mục hiện hành hoặc `data/`; nếu nạp qua data asset, dùng đoạn code truy cập file mà IBM cung cấp để đọc CSV với `sep=';'`.
4. Bảo đảm helper `cardio_utils.py` nằm cùng thư mục làm việc, hoặc đưa class IQRClipper trong file này vào cell đầu. Cài các thư viện chưa có.
5. Chạy lại toàn bộ notebook, lưu notebook có outputs và biểu đồ. Bản đính kèm đã chạy local, nên cần bước này để có minh chứng Watson thật.
6. Tương tự nhập notebook 01 nếu thực hiện truy vấn Db2 trong Watson. Cung cấp credentials riêng trong biến môi trường/secret của project.
7. Xuất notebook đã chạy và các kết quả; đưa vào GitHub. Không gọi gói này là file project ZIP gốc của Watson: đây là ZIP thư mục bài tập thông thường.

## Tải lên GitHub bằng Chrome
1. Giải nén ZIP trên máy; đăng nhập GitHub bằng tài khoản của bạn.
2. Tạo repository, ví dụ `ADY201m-Cardio-Assignment`; chọn riêng tư nếu muốn, và cấp quyền xem theo yêu cầu giảng viên.
3. Trong repository, chọn Add file → Upload files. Kéo các file/thư mục đã giải nén vào (không chỉ tải một file ZIP).
4. Tải README, hai `.ipynb`, hai `.html`, báo cáo HTML, requirements, helper, SQL, CSV và kết quả. Các file đều dưới giới hạn 25 MB của upload web.
5. Viết commit message, ví dụ `Complete offline cardiovascular analysis and Db2 query notebooks`, rồi commit.
6. Mở từng notebook trên GitHub để kiểm tra hiển thị. Khi đã chạy Cloud, thay notebook local bằng bản Cloud có outputs và bổ sung minh chứng thật.
7. Không tải hai PDF gốc nếu không cần; các file gốc có thông tin đăng nhập mẫu và có thể bị giới hạn kích thước.

## Kết quả thực tế
- Mô hình chọn theo CV: GradientBoosting tuned (CV).
- CV Accuracy train: 73.69%; test Accuracy: 73.04%.
- Test Precision: 74.55%; Recall: 69.94%; F1: 72.17%; ROC-AUC: 79.81%.
- Chia 49.000 train / 21.000 test, random_state=42, stratify theo nhãn.
- Các ngưỡng IQR và StandardScaler của mô hình được học chỉ trên train; CV dùng pipeline để tránh rò rỉ.
- Các nhóm 10 hồ sơ được chọn theo ORDER BY xác định, nên một số tỷ lệ có thể khác ví dụ đề.
- ANOVA/T-test/OLS được giữ theo đề; không diễn giải tương quan thành nguyên nhân bệnh.

## Đối chiếu yêu cầu
| Yêu cầu | File/minh chứng | Trạng thái |
|---|---|---|
| Tìm hiểu dữ liệu | Notebook 02, extraction_audit.json | Đã chạy |
| Upload Db2 và SQL console | sql/ và notebook 01 | Code hoàn tất; cần kết nối tài khoản IBM |
| Python ibm_db và 10 truy vấn | Notebook 01 | SELECT local đã chạy; kết nối Db2 chưa chạy |
| Xuất CSV và đóng kết nối | Notebook 01 | Đã chạy local |
| EDA, IQR, kiểm định, OLS | Notebook 02 | Đã chạy |
| RidgeClassifier và các mô hình mẫu | Notebook 02 | Đã chạy |
| Tinh chỉnh mô hình | GridSearchCV và results/grid_search.csv | Đã chạy |
| Thực hiện lại Watson Studio | Hướng dẫn trên | Chưa chạy |
| Upload GitHub | anhcumoc4231/ADY201m-Cardio-Assignment | Đã tải, repository riêng tư |

## Nguồn
- Đề ADY201m và PDF cardio_train_raw do người dùng cung cấp.
- https://www.ibm.com/docs/en/db2/12.1.0?topic=db-connecting-database-server
- https://www.ibm.com/docs/en/ws-and-kc?topic=editor-creating-managing-notebooks
- https://www.ibm.com/docs/en/ws-and-kc?topic=scripts-loading-accessing-data-in-notebook
- https://scikit-learn.org/1.8/common_pitfalls.html
