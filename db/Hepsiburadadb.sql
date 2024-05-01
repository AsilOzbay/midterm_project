CREATE TABLE hepsiburada (
  id int PRIMARY KEY,
  fiyat int,
  isim varchar(45) NOT NULL,
  kategori varchar(45) NOT NULL,
  yıl int,
  kapıda_ödeme_türü tinyint,
  şehir varchar(45) NOT NULL,
  resim BLOB
);
