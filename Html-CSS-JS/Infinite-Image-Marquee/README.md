# 🖼️ Infinite Image Scroll - Módulo de Rolagem Infinita de Imagens 🌟

Bem-vindo ao Infinite Image Scroll! Este módulo faz parte do repositório Html-CSS-JS e implementa um efeito de rolagem contínua para imagens, criando um movimento visual de "loop infinito". A rolagem é suave e pode ser facilmente personalizada para atender às suas necessidades.
## 📌 Funcionalidades

✅ Rolagem contínua de imagens, criando um efeito de loop infinito.<br>
✅ Flexibilidade para adicionar ou remover logos/imagens.<br>
✅ Suporte a diferentes tamanhos de tela com responsividade.<br>
✅ Efeito de transição suave para uma experiência visual agradável.

## 📂 Estrutura do Código

- `index.html` → Implementação do HTML, CSS e JS para a rolagem infinita de imagens.
- `style.css` →  Arquivo de estilos que controla a aparência e a responsividade.
- `script.js` → Script que cria a animação de rolagem infinita de imagens.

## 📦 Instalação

1️⃣ Clone o repositório:
```sh
git clone https://github.com/seu-usuario/repositorio
cd Html-CSS-JS/infinite-image-scroll

```

2️⃣ Abra o arquivo index.html em seu navegador para visualizar o efeito.

## 🚀 Como Usar

### 🔹 Como Personalizar
1️⃣ Adicionar novas imagens

Você pode adicionar novas imagens ao loop infinito inserindo tags img dentro da div com a classe marquee-content. Exemplo:

```html
<img src="nova-imagem.png" alt="Nova Imagem" />
```
2️⃣ Alterar a velocidade da rolagem

A velocidade da rolagem é controlada pela animação CSS definida na propriedade animation do .marquee-wrapper. O valor atual é 60s:

```css
animation: scroll 60s linear infinite;
```
Responsividade:

O código já possui pontos de quebra (media queries) para garantir que o efeito funcione bem em diferentes tamanhos de tela. Você pode ajustar os tamanhos das imagens dentro dessas media queries conforme necessário.
### 🔹 Exemplo de Uso

### HTML

```html
<div class="logo-marquee-container">
  <div class="marquee-wrapper" id="marquee-wrapper">
    <div class="marquee-content">
      <img src="assests/logos/logo1.png" alt="Logo 1"/>
      <img src="assests/logos/logo2.png" alt="Logo 2"/>
      <!-- Mais imagens -->
    </div>
  </div>
</div>
```
### SCRIPT

```html
const marqueeWrapper = document.getElementById("marquee-wrapper");
const marqueeContent = marqueeWrapper.querySelector(".marquee-content");

// Clona o conteúdo das logos
const clone = marqueeContent.cloneNode(true);

// Adiciona a cópia ao wrapper
marqueeWrapper.appendChild(clone);

```
## 🛠️ Tecnologias Utilizadas

- **HTML5**
- **CSS3**
- **Java Script**
- **Responsividade  (Media Queries)**

## 📜 Licença

Este projeto está licenciado sob a **MIT License** - consulte o arquivo `LICENSE` para mais detalhes.

---
📢 **Contribuições são bem-vindas!** Se você tem sugestões ou melhorias, fique à vontade para abrir um pull request. 😊

