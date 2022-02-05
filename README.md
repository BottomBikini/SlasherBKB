Склейка и растрирование.
1 — Загрузка

Я не буду рассказывать про обыкновенные способы склейки и резки. Но хочу поделиться очень быстрым и эффективным способом, над которым постаралась наша команда. Программа сама склеивает, определяет пустоту между фреймами и режет их.
Мы будем все делать в одной программе.
Но для начала скачиваем программу:
Links: GitHub
Download: GitHub | GoogleDisk
После установки программы, открываем ее. 

Настройки:
https://github.com/BottomBikini/SlasherBKB/raw/main/Logo/image.png
1) Обзор — мы выбираем папку со сканами которые нам нужно склеить и разрезать.
2 — Базовые настройки
2.1 ) «Высота скана» ( Мы указываем не высоту всего скана, а по сколько пикселей в высоту программа должна порезать.) 
Пример: У нас есть скан в высоту 90000 — и мы укажем значение 20000, то получим: 90000/20000=4 — 5 сканов на выходе. Может быть меньше или больше, это все из-за того что скрипт определяет пустую область между фреймами, и может порезать 1 скан, не в 20000px, а в 22000px.
2.2 ) «Кол-во сканов на выходе» — тут все проще, просто указываем сколько страниц нам нужно, программа сама склеит и разрежет. 
3) «Тип изображения» — Какой тип у сканов должен быть после склейки и растрирования ( .png / .jpg / .webp / .bmp / .tiff / .tga )
4) Расширенные настройки — «Чувствительность обнаружения пустоты» — Это значение влияет на то, на сколько точно программа будет обнаруживать пустые области между фреймами. ( Не рекомендую ставить значение меньше 90%.)
С настройками мы разобрались, теперь приступим к сути.
Выберем папку ( Не открывайте ее, нам нужно выбрать именно папку )
со сканами, для этого нажмем кнопку «Обзор»
 
После того как мы выбрали нужную папку, нажимаем «Выбор папки».
 
Далее, мы должны выбрать сколько страниц нам нужно на выходе. Включаем галочку — «Кол-во сканов на выходе» и указываем нужное нам значение.
( Если мы укажем значение «1» то все склеиться в один скан.)
 
Указываем нужный нам тип изображения :
 
Включаем расширенные настройки и в строке «Чувствительность обнаружения пустоты» ставим значение не ниже 90% — рекомендовано.
 
Все, больше мы ничего не трогаем и можем нажимать кнопку «ПОПЛЫЛИ»
После некоторого времени, программа выдаст вам строку о успешной (или нет) завершении работы. 
 
Готовые (-ый) сканы будут в той же директории где вы выбирали папку со сканами, и будет добавлен текст [ Разрезано ]
 
 

