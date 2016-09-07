# WaterMarkPy
Add watermark in multiple images at once.

##WaterMarkPy permite adicionar marcas d'águas em imagens
Para adicionar a marca no centro de UMA imagem, execute:
> python main.py -i nomeImagem.bmp -w nomeWM.png -o nomeSaida

Para adicionar a marca no centro de diversas imagens em um diretorio, execute:
> python main.py -d imgs/ -w nomeWM.png

Para alterar o tamanho da marca (escala (em %)) e definir a margem TOP (em %) e LEFT(em %) do local da marca em UMA imagem, execute:
> python main.py -i imgs/nomeImagem.bmp -w nomeWM.png -s 10 -mt 25 -ml 25 -o nomeSaida

Para alterar o tamanho da marca (escala (%)) e definir a margem TOP (%) e LEFT (%) do local da marca em varias imagens em um diretorio, execute:
> python main.py -d imgs/ -w nomeWM.png -s 30 -mt 25 -ml 25

Parametros: 

> -i Nome da imagem principal.               ex: -i imagem/img.bmp

> -w Nome da imagem da watermark.            ex: -i imagem/wm.bmp

> -d Diretorio com imagens sem a marca.      ex: -d imagem/

> -s scale (em %) da marca em relacao ao     ex: -s 30
tamanho da imagem principal."

> -mt Margem TOP em %.                       ex: -mt 20

> -ml Margem LEFT em %.                      ex: -ml 20

> -p Adicionar um prefixo no nome da imagem. ex: -p water
