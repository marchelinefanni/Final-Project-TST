# Final-Project-TST
18221090 - Marcheline Fanni Hidayat Putri <br>
Final Project (Phase 1): Microservice Deployment of Fashion Upcycling Service
<br>
## Deskripsi Layanan
`FashUp` adalah layanan yang memungkinkan penggunanya untuk melakukan upcycling produk tekstil lama menjadi sebuah produk baru yang memiliki nilai lebih. Core service dari FashUp adalah `pemesanan (order)` yang disertai dengan `rekomendasi produk` dan `estimasi kuantitas` berdasarkan bahan (material) dan berat (weight). Pengguna dapat membuat pemesanan, melihat pemesanan, mengubah pemesanan, dan menghapus pemesanan. Data yang dibutuhkan untuk melakukan pemesanan adalah ID pemesanan, bahan, berat, produk yang diinginkan, dan kuantitas produk. Untuk membantu pengguna menentukan pilihan produk, pengguna dapat memanfaatkan rekomendasi yang telah dibangun berdasarkan bahan yang dimiliki oleh pengguna. Selain itu, terdapat kalkulator kuantitas produk yang dapat mengestimasi jumlah produk yang dapat diperoleh dari berat bahan yang dimiliki. 
<br>
## Spesifikasi Layanan
Layanan ini dibangun menggunakan teknologi berikut ini:
* FastAPI 0.104.1
* Pydantic 2.4.2
* Uvicorn 0.24.0
<br>
Layanan ini memiliki total `10 API Endpoints` sebagai berikut:
1. Welcome 
2. Create Order
3. Read All Order
4. Read Order
5. Read All Materials
6. Read All Catalogue
7. Update Order
8. Delete Order
9. Product Recommendation
10. Quantity Calculator    
<br>
## Cara Menjalankan Layanan
Menjalankan secara lokal dengan uvicorn
1. Jalankan terminal
2. Lakukan instalasi Fast API dengan pip install fastapi
3. Lakukan instalasi pydantic dengan pip install pydantic
4. Lakukan instalasi uvicorn dengan pip install uvicorn
5. Jalankan program dengan uvicorn main:app --reload
<br>
Menjalankan secara lokal menggunakan docker
1. Unduh dan lakukan pengaturan docker pada perangkat
2. Jalankan command berikut ini pada terminal:
   docker build -t <image_name> .
   docker run -d --name <container_naem> -p 80:80 <image_name>
<br>
Menjalankan melalui layanan azure
1. Buka link berikut ini: http://fashup2.ayfeg8ebcpc3gfbn.southeastasia.azurecontainer.io/docs
2. Mencoba setiap API endpoint yang tersedia dengan menekan opsi try it out dan memasukkan input jika diperlukan

