
# Kaip pasirinkti repo:

su cd nueiti i Projekto folderi savo kompe

pvz: C:\Users\tikta\Downloads\Python-project\simple-calculator-tkinter-master

# tada:

git init 

git remote add origin https://github.com/Tomas-Seikauskas/Python-project.git

git branch -M main

# Kaip addinti i git:

git add .

git commit -m "pvz"

git push -u origin main

# Jeigu neveikia/yra errors:
git status

git checkout --ours .

git add .

git commit -m "pvz"

git push -u origin main