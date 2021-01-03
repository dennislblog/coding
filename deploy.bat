@echo off

echo building...
call yarn build
echo building complete...

cd docs/.vuepress/dist
git init
git add -A
git commit -m 'auto-deploy'
git push -f git@github.com:dennislblog/coding.git master:gh-pages