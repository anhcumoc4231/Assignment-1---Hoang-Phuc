# ADY201m — Phân tích và dự đoán bệnh tim mạch

Repository trình bày bài tập phân tích dữ liệu bệnh tim mạch thuộc học phần ADY201m. Nội dung bao gồm truy vấn SQL, xử lý dữ liệu bằng Python, phân tích khám phá, kiểm định thống kê và so sánh các mô hình phân loại nhãn `CARDIO`.

## Phạm vi và trạng thái thực hiện

Quy trình phân tích và huấn luyện đã được thực thi trên môi trường cục bộ. Hai notebook lưu mã nguồn, kết quả truy vấn, bảng thống kê và biểu đồ để phục vụ đánh giá và tái lập.

**Phương án thay thế đã được giảng viên chấp nhận:** sử dụng SQLite để lưu trữ, truy vấn dữ liệu và thực hiện notebook trên môi trường cục bộ. Cơ sở dữ liệu được lưu tại `data/cardio_train.sqlite`, tiếp tục tồn tại sau khi đóng kết nối hoặc kết thúc phiên notebook.

Notebook 01 đã thực thi 13 SELECT trên cơ sở dữ liệu này, xuất CSV và kiểm tra dữ liệu sau khi mở lại tệp. Nhánh IBM Db2 và hướng dẫn Watson Studio được giữ để tham khảo tùy chọn; các kết quả đính kèm phản ánh thực thi cục bộ, không phải thực thi trên IBM Cloud.

## Dữ liệu

Dữ liệu được khôi phục từ tài liệu PDF của bộ dữ liệu `cardio_train_raw` kèm đề bài và kiểm tra trước khi phân tích.

| Thuộc tính | Giá trị |
|---|---:|
| Số bản ghi | 70.000 |
| Số cột | 13 |
| Số đặc trưng đầu vào | 11 |
| Bản ghi có `CARDIO = 1` | 34.979 |
| Bản ghi có `CARDIO = 0` | 35.021 |

`ID` là mã hồ sơ, không được sử dụng làm đặc trưng dự đoán. Tuổi trong dữ liệu gốc tính bằng ngày; quy trình phân tích chuyển tuổi sang năm nguyên bằng phép chia `AGE // 365`.

| Tệp dữ liệu | Nội dung |
|---|---|
| `data/cardio_train.sqlite` | Cơ sở dữ liệu SQLite lưu bền vững; bảng `CARDIO_TRAIN` gồm 70.000 hồ sơ, có khóa chính `ID`. |
| `data/cardio_train_raw.csv` | Dữ liệu gốc; phân cách bằng dấu chấm phẩy; tuổi tính bằng ngày. |
| `data/CARDIO_TRAIN_export.csv` | Dữ liệu xuất từ truy vấn SQL cục bộ; phân cách bằng dấu phẩy; tuổi tính bằng ngày. |
| `data/cardio_train_clean.csv` | Dữ liệu phục vụ EDA và thống kê sau xử lý IQR; tuổi tính bằng năm. |
| `data/extraction_audit.json` | Thông tin kiểm tra quá trình khôi phục dữ liệu từ PDF. |

Notebook phân tích đọc dữ liệu **gốc**. Tệp đã làm sạch không được dùng thay thế dữ liệu đầu vào này, nhằm tránh chuyển đổi tuổi hai lần và sử dụng các ngưỡng IQR tính trên toàn bộ dữ liệu trong huấn luyện.

## Cấu trúc repository

```text
.
├── 01_Db2_SQL_Python.ipynb       # SQL, kết nối Python và xuất dữ liệu
├── 02_Cardio_Analysis_ML.ipynb   # EDA, kiểm định và mô hình phân loại
├── 01_Db2_SQL_Python.html        # Bản xem notebook SQL
├── 02_Cardio_Analysis_ML.html    # Bản xem notebook phân tích
├── Bao_cao_ADY201m.html          # Báo cáo tiếng Việt, tự chứa biểu đồ
├── cardio_utils.py              # Bộ xử lý IQR dùng trong pipeline
├── sqlite_storage.py            # Tạo, mở lại và kiểm tra cơ sở dữ liệu SQLite
├── requirements.txt            # Các thư viện và phiên bản môi trường
├── data/                       # Cơ sở dữ liệu SQLite, CSV và kiểm tra nguồn
├── sql/                        # DDL và 13 SELECT cho SQLite; bản Db2 tham khảo
├── figures/                    # Chín biểu đồ từ notebook phân tích
├── results/                    # Thống kê, mô hình và kết quả đánh giá
└── MANIFEST.json                # Kích thước và SHA-256 của các tệp
```

Báo cáo HTML và các bản HTML của notebook có thể mở trực tiếp bằng trình duyệt sau khi tải xuống. Hai tệp `.ipynb` có thể xem kết quả ngay trên GitHub.

## Phương pháp

1. Kiểm tra cấu trúc dữ liệu, miền giá trị và phân bố nhãn.
2. Tạo bảng SQL với khóa chính `ID` và ràng buộc mã phân loại; nhập dữ liệu một lần vào tệp SQLite. Những lần chạy tiếp theo kiểm tra và sử dụng lại bảng có sẵn, không xóa hoặc nhân đôi các hồ sơ.
3. Thực hiện 13 truy vấn SELECT; Q01–Q10 tương ứng 10 yêu cầu truy vấn bằng API Python trong đề bài. Các nhóm giới hạn 10 hồ sơ sử dụng `ORDER BY` để bảo đảm kết quả xác định.
4. Phân tích khám phá bằng thống kê mô tả, histogram, heatmap, regplot và boxplot.
5. Xử lý ngoại lệ huyết áp tâm thu và tâm trương bằng chặn IQR; thực hiện ANOVA, Levene/T-test, Pearson, Chi-square và OLS theo nội dung đề bài.
6. Chia dữ liệu thành 49.000 hồ sơ huấn luyện và 21.000 hồ sơ kiểm tra, phân tầng theo nhãn với `random_state = 42`.
7. So sánh RidgeClassifier, AdaBoost, Gradient Boosting, Random Forest, Bagging KNN, Extra Trees và Stacking, cùng mô hình dự đoán lớp phổ biến làm mốc so sánh.
8. Tinh chỉnh Gradient Boosting bằng `GridSearchCV` với 8 tổ hợp tham số và 3 fold trên tập huấn luyện.

Trong quy trình mô hình, các ngưỡng IQR và tham số chuẩn hóa chỉ được học trên dữ liệu huấn luyện của từng lần fit. Các bước tiền xử lý nằm trong pipeline, bao gồm cả quá trình cross-validation. Ngưỡng IQR tính trên toàn bộ dữ liệu chỉ phục vụ EDA và thống kê.

## Kết quả đánh giá

Mô hình được chọn theo cross-validation trên tập huấn luyện là **Gradient Boosting đã tinh chỉnh**. Accuracy trung bình tốt nhất trong cross-validation đạt **73,69%**.

| Chỉ số trên tập kiểm tra | Giá trị |
|---|---:|
| Accuracy | 73,04% |
| Precision | 74,55% |
| Recall | 69,94% |
| F1-score | 72,17% |
| ROC-AUC | 79,81% |

Mô hình được chọn trước khi đánh giá trên tập kiểm tra. Bảng so sánh đầy đủ nằm trong `results/model_comparison.csv`; kết quả tìm kiếm tham số nằm trong `results/grid_search.csv`. Điểm kiểm tra cao nhất trong bảng so sánh không được dùng để chọn lại mô hình hoặc tham số.

Các kết quả bổ sung được lưu trong `results/`: kiểm định thống kê, hệ số OLS, mức đóng góp đặc trưng, ID của tập huấn luyện/kiểm tra, dự đoán và mô hình đã lưu.

## Đối chiếu yêu cầu bài tập

| Yêu cầu | Tệp hoặc minh chứng | Trạng thái |
|---|---|---|
| Tìm hiểu và kiểm tra dữ liệu | Notebook 02; `data/extraction_audit.json` | Đã thực thi cục bộ |
| Tạo bảng, nhập dữ liệu và chạy SQL | `data/cardio_train.sqlite`; `sql/03_create_table_sqlite.sql`; `sql/04_queries_sqlite.sql` | Đã thực thi bằng SQLite theo phương án thay thế được chấp nhận |
| Kết nối Python và thực hiện 10 truy vấn | Notebook 01; `results/db_execution_status.json` | Đã thực thi bằng `sqlite3`; có thêm 3 truy vấn bổ sung |
| Xuất CSV và đóng kết nối | Notebook 01 | Đã thực thi cục bộ |
| EDA, IQR, kiểm định và OLS | Notebook 02 | Đã thực thi cục bộ |
| Huấn luyện và so sánh các mô hình | Notebook 02; `results/model_comparison.csv` | Đã thực thi cục bộ |
| Tinh chỉnh mô hình | Notebook 02; `results/grid_search.csv` | Đã thực thi cục bộ |
| Môi trường notebook phân tích | Notebook 02 | Đã thực thi cục bộ theo phương án thay thế được chấp nhận |
| Lưu trữ bài tập trên GitHub | Repository này | Đã hoàn tất |

## Tái lập trên môi trường cục bộ

Môi trường sử dụng Python 3.12. Thực hiện các lệnh sau tại thư mục gốc của repository:

```bash
python -m pip install -r requirements.txt
python -m notebook
```

Chạy lần lượt notebook 01 và notebook 02. Notebook 01 mặc định sử dụng tệp SQLite với `RUN_DB2 = 0`; notebook 02 thực hiện phân tích và huấn luyện từ dữ liệu gốc. Không cần tài khoản IBM để tái lập phương án này.

Notebook 01 tạo cơ sở dữ liệu khi bảng chưa tồn tại; nếu bảng đã tồn tại, toàn bộ hồ sơ được đối chiếu với CSV gốc trước khi truy vấn. Có thể cấu hình vị trí tệp khác bằng biến môi trường `SQLITE_DB_PATH`.

`cardio_utils.py` phải nằm trong thư mục làm việc hoặc trong đường dẫn import để thực thi pipeline và nạp mô hình `results/cardio_classifier.joblib`. Các phiên bản thư viện được ghi trong `requirements.txt` và `results/environment_versions.csv`.

## Kiểm tra cơ sở dữ liệu đã lưu

Từ thư mục gốc repository, có thể mở lại tệp bằng Python:

```python
import sqlite3

connection = sqlite3.connect("data/cardio_train.sqlite")
print(connection.execute("SELECT COUNT(*), SUM(CARDIO) FROM CARDIO_TRAIN").fetchone())
print(connection.execute("PRAGMA integrity_check").fetchone())
connection.close()
```

Kết quả mong đợi là `(70000, 34979)` và `('ok',)`. Kết quả kiểm tra thực tế sau khi đóng và mở lại kết nối nằm trong `results/db_execution_status.json`.

`sql/04_queries_sqlite.sql` chứa các SELECT có thể thực thi trực tiếp trên tệp SQLite. Mỗi truy vấn được ghi rõ mã Q01–Q13 và nội dung tương ứng.

## IBM Cloud — phương án tham khảo tùy chọn

### IBM Db2

Điều kiện thực thi là tài khoản IBM Cloud đã kích hoạt và dịch vụ Db2 có quyền nạp dữ liệu, truy vấn.

1. Thực thi `sql/01_create_table.sql` trong schema được cấp quyền.
2. Nhập `data/cardio_train_raw.csv` với dấu phân cách `;` và dòng đầu chứa tên cột; giữ nguyên `AGE` theo ngày.
3. Thực thi `sql/02_queries.sql`; kiểm tra tổng số 70.000 hồ sơ và 34.979 hồ sơ có `CARDIO = 1`.
4. Cài thư viện kết nối bằng `python -m pip install ibm_db`.
5. Thiết lập các biến môi trường `DB2_DATABASE`, `DB2_HOSTNAME`, `DB2_PORT`, `DB2_UID`, `DB2_PWD` và `RUN_DB2 = 1`. Thiết lập `DB2_SSL_CERT` nếu dịch vụ yêu cầu chứng thư.
6. Chạy toàn bộ notebook 01. Nếu bảng thuộc schema khác schema mặc định, điều chỉnh tên bảng thành `SCHEMA.CARDIO_TRAIN`.
7. Lưu notebook có kết quả kết nối, truy vấn và xuất dữ liệu; trạng thái `cloud_executed` phải phản ánh lần thực thi thực tế.

Thông tin kết nối được cung cấp qua biến môi trường hoặc cơ chế quản lý secret. Mật khẩu, access token và khóa riêng không được lưu trong mã nguồn hoặc kết quả notebook.

### Watson Studio / watsonx.ai Studio

1. Tạo hoặc mở project có môi trường notebook phù hợp.
2. Nhập notebook 02, dữ liệu gốc và `cardio_utils.py` vào môi trường thực thi.
3. Đặt CSV gốc tại thư mục hiện hành hoặc `data/`; nếu sử dụng data asset, điều chỉnh đoạn đọc dữ liệu theo cơ chế truy cập của project và giữ `sep=';'`.
4. Cài các thư viện còn thiếu, chạy toàn bộ notebook và lưu kết quả cùng biểu đồ.
5. Nhập notebook 01 nếu truy vấn Db2 được thực hiện trong cùng project; cung cấp thông tin kết nối bằng biến môi trường hoặc secret.
6. Xuất notebook đã thực thi để cập nhật repository và bổ sung minh chứng môi trường Cloud.

## Giới hạn và lưu ý diễn giải

- Các kiểm định phản ánh mối liên hệ thống kê trên dữ liệu quan sát, không chứng minh quan hệ nhân quả. P-value cần được đọc cùng độ lớn hiệu ứng.
- OLS được sử dụng để tái hiện nội dung thống kê của đề; bộ phân loại cuối xử lý nhãn nhị phân `CARDIO`.
- Các hồ sơ trùng đặc trưng được giữ lại do có ID riêng và chưa đủ căn cứ xác định cùng một cá nhân.
- Kết quả có thể khác ví dụ minh họa trong đề do thứ tự truy vấn, cách chia dữ liệu và phiên bản thư viện.
- Mô hình phục vụ mục đích học tập; chưa được kiểm định cho chẩn đoán lâm sàng.

## Tài liệu tham khảo

- Đề bài ADY201m và tài liệu PDF của bộ dữ liệu `cardio_train_raw` kèm theo đề.
- [Python — Kết nối, truy vấn và lưu trữ SQLite bằng sqlite3](https://docs.python.org/3/library/sqlite3.html).
- [IBM — Kết nối Db2 bằng Python](https://www.ibm.com/docs/en/db2/12.1.0?topic=db-connecting-database-server).
- [IBM — Tạo và quản lý notebook](https://www.ibm.com/docs/en/ws-and-kc?topic=editor-creating-managing-notebooks).
- [IBM — Nạp và truy cập dữ liệu trong notebook](https://www.ibm.com/docs/en/ws-and-kc?topic=scripts-loading-accessing-data-in-notebook).
- [scikit-learn — Các lỗi thường gặp và tránh rò rỉ dữ liệu](https://scikit-learn.org/1.8/common_pitfalls.html).
