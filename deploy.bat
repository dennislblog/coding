@echo off

echo push master
git add -A
git commit -m "%~1"
git push origin master
echo push master complete...


echo building...
call yarn build
echo building complete...

cd docs/.vuepress/dist
git init
touch .gitignore && echo private* > .gitignore
git add -A
git commit -m 'auto-deploy'
git push -f git@github.com:dennislblog/coding.git master:gh-pages