# Football Maydonini buyurtma qilish

API:
   /stadium/find/ methods ['GET'] - Yaqin oradagi va bo'sh stadionalrni topish uchun
   /stadium/booking/ methods ['GET', 'POST'] - Yaqin oradagi va bo'sh stadionalrni buyurtma qilish uchun,band maydonlarni 
   buyurtma qilib bo'lmaydi



P.S Bu loyihada sqlite ma'lumotlar bazasi sifatida foydalanildi, sababi "render.com" da Postgresql instance uchun obuna tugaganligi
Media fayllar saqlashda kod lokalhostda to'g'ri ishlaydi  lekin meda fayllarni alohida diskda bo'lmasa render.com qabul qilmaydi
shu sababdan serverda AWS S3 yoki boshqa fayl saqlash tizimidan foydalanish maslahat beriladi
   
