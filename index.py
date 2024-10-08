import turtle
import random

# Configurações da tela
screen = turtle.Screen()
screen.title("Jogo do Peixe que Nada e Salta")
screen.setup(width=800, height=600)
screen.bgpic("bottom.gif")  # Defina a imagem de fundo com algas
screen.bgcolor("lightblue")  # Cor de fundo de backup, se necessário

# Registrar as imagens
screen.addshape("fish.gif")  # Usar imagem do peixe
screen.addshape("heart.gif")  # Usar imagem do coração
screen.addshape("bubble.gif")  # Usar imagem da bolha

# Criar o jogador usando a imagem do peixe
player = turtle.Turtle()
player.shape("fish.gif")  # Usar imagem personalizada
player.penup()
player.goto(-300, 0)  # Posiciona o peixe mais à esquerda da tela

# Variáveis de movimento e pontuação
player_speed_y = 0
gravity = -1  # Gravidade que puxa o peixe para baixo
jump_strength = 15  # Força do pulo
bubble_speed = 5  # Velocidade da bolha
heart_speed = 7  # Velocidade dos corações
score = 0  # Inicializa a pontuação

# Criar a bolha
bubble = turtle.Turtle()
bubble.shape("bubble.gif")  # Usar imagem da bolha
bubble.penup()
bubble.goto(400, random.randint(-250, 250))  # Posição inicial da bolha à direita
bubble.speed(0)

# Função para mover a bolha
def move_bubble():
    global score

    # Mover a bolha para a esquerda
    bubble.setx(bubble.xcor() - bubble_speed)

    # Verificar colisão com o peixe
    if player.distance(bubble) < 30:  # Distância de colisão ajustada
        print("Colisão com a bolha! Fim de Jogo!")
        score_display.clear()
        score_display.write("Fim de Jogo!", align="left", font=("Arial", 24, "normal"))
        draw_restart_button()  # Chama a função para desenhar o botão de reiniciar

    # Reposicionar a bolha quando sair da tela
    if bubble.xcor() < -400:
        bubble.goto(400, random.randint(-250, 250))  # Voltar para a direita com nova altura

    # Continuar chamando essa função repetidamente
    screen.ontimer(move_bubble, 20)

# Função para fazer o peixe pular
def jump():
    global player_speed_y
    player_speed_y = jump_strength

# Função que move o peixe e aplica gravidade
def move_player():
    global player_speed_y

    # Atualizar a velocidade vertical do peixe (gravidade)
    player_speed_y += gravity
    new_y = player.ycor() + player_speed_y

    # Impedir que o peixe saia pela parte inferior ou superior da tela
    if new_y < -280:
        new_y = -280  # Limitar o peixe na parte inferior
        player_speed_y = 0  # Parar o movimento para baixo ao tocar o chão
    elif new_y > 280:
        new_y = 280  # Limitar o peixe na parte superior

    player.sety(new_y)

    # Continuar chamando essa função repetidamente
    screen.ontimer(move_player, 20)

# Função para criar um novo coração que surge do lado direito e se move para a esquerda
def create_heart():
    heart = turtle.Turtle()
    heart.shape("heart.gif")  # Usar imagem do coração
    heart.penup()
    
    # Posição inicial na borda direita da tela
    heart.goto(400, random.randint(-250, 250))  # Aleatório na altura
    hearts.append(heart)  # Adiciona o coração à lista
    move_hearts()  # Chama a função de mover corações para que não haja pausa

# Criar a lista para os corações (inicialmente vazia)
hearts = []

# Função para mover os corações da direita para a esquerda
def move_hearts():
    global score
    hearts_to_remove = []
    
    for heart in hearts:
        # Mover o coração para a esquerda
        heart.setx(heart.xcor() - heart_speed)  # Velocidade de movimento do coração
        
        # Verificar colisão com o jogador
        if player.distance(heart) < 30:  # Distância de colisão ajustada
            heart.hideturtle()  # Esconde o coração (estoura)
            hearts_to_remove.append(heart)  # Adiciona o coração para remoção
            score += 1  # Ganha 1 ponto
            print("Coletou um coração! Pontuação:", score)
            score_display.clear()
            score_display.write(f"Pontuação: {score}", align="left", font=("Arial", 24, "normal"))
        
        # Remover o coração se ele sair da tela pela esquerda
        if heart.xcor() < -400:
            hearts_to_remove.append(heart)

    # Remover corações que foram coletados ou saíram da tela
    for heart in hearts_to_remove:
        hearts.remove(heart)

    # Continuar chamando essa função repetidamente
    screen.ontimer(move_hearts, 50)

# Função para adicionar corações gradativamente
def add_heart():
    if len(hearts) < 5:  # Limita para que tenha até 5 corações ao mesmo tempo
        create_heart()  # Chama a função que cria um coração
    
    # Continuar chamando essa função repetidamente para adicionar corações ao longo do tempo
    screen.ontimer(add_heart, random.randint(500, 2000))  # Corações surgem entre 0,5 e 2 segundos de diferença

# Criar e exibir a pontuação
score_display = turtle.Turtle()
score_display.hideturtle()
score_display.penup()
score_display.goto(-350, 250)
score_display.write(f"Pontuação: {score}", align="left", font=("Arial", 24, "normal"))

# Função para desenhar o botão de reiniciar
def draw_restart_button():
    button = turtle.Turtle()
    button.hideturtle()
    button.penup()
    button.goto(0, -50)  # Posição do botão
    button.color("orange")
    button.begin_fill()
    
    # Desenhar um retângulo
    for _ in range(2):  
        button.forward(150)
        button.right(90)
        button.forward(50)
        button.right(90)
    button.end_fill()

    button.goto(0, -30)
    button.color("black")
    button.write("Iniciar Novamente", align="center", font=("Arial", 18, "normal"))

    # Lidar com o clique no botão
    screen.onclick(lambda x, y: restart_game() if -75 < x < 75 and -50 < y < 0 else None)

# Função para reiniciar o jogo
def restart_game():
    global score
    score = 0
    score_display.clear()
    score_display.write(f"Pontuação: {score}", align="left", font=("Arial", 24, "normal"))
    
    # Reiniciar o jogador
    player.goto(-300, 0)
    
    # Limpar corações existentes
    for heart in hearts:
        heart.hideturtle()
    hearts.clear()
    
    # Reiniciar a bolha
    bubble.goto(400, random.randint(-250, 250))

    # Remover o botão de reiniciar
    screen.clear()  # Limpar a tela para reiniciar completamente
    screen.bgpic("bottom.gif")  # Redefinir o fundo
    screen.addshape("fish.gif")  # Re-add shapes
    screen.addshape("heart.gif") 
    screen.addshape("bubble.gif") 
    draw_restart_button()  # Redesenhar o botão

    # Iniciar novamente os movimentos
    move_player()
    move_bubble()
    add_heart()

# Ligar a tecla de espaço para fazer o peixe pular
screen.listen()
screen.onkey(jump, "space")

# Iniciar o movimento do peixe, da bolha, corações e verificar colisões
move_player()
move_bubble()
add_heart()  # Inicia a adição de corações gradativamente

# Loop principal
screen.mainloop()






