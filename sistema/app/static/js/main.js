const ENDPOINT_PRODUTOS = "/produtos/";

const container = document.getElementById("lista-produtos");
const contagemEl = document.getElementById("contagem-produtos");
const listaCategorias = document.getElementById("lista-categorias");

let produtosCarregados = [];
let categoriaAtiva = "todos";

const ICONE_CARRINHO = `
  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M3 3h2l.4 2M7 13h10l3-8H5.4M7 13L5.4 5M7 13l-2.3 4.6A1 1 0 0 0 5.6 19H17M17 19a2 2 0 1 0 0 4 2 2 0 0 0 0-4ZM9 19a2 2 0 1 0 0 4 2 2 0 0 0 0-4Z"
      stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  </svg>
`;

function formatarPreco(preco) {
    const numero = Number(preco);
    if (Number.isNaN(numero)) return "Sob consulta";
    return numero.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
}

function imagemUrlSegura(url) {
    if (!url) return "";
    return encodeURI(url)
        .replace(/\(/g, "%28")
        .replace(/\)/g, "%29")
        .replace(/'/g, "%27");
}

function adicionarAoCarrinhoRapido(produto) {
    const CHAVE = "inovatech_carrinho";
    let carrinho = [];
    try {
        carrinho = JSON.parse(localStorage.getItem(CHAVE)) || [];
    } catch (e) {
        carrinho = [];
    }

    const existente = carrinho.find((item) => item.id_produto === produto.id_produto);
    if (existente) {
        existente.quantidade += 1;
    } else {
        carrinho.push({
            id_produto: produto.id_produto,
            nome: produto.nome,
            preco: Number(produto.preco),
            imagem_url: produto.imagem_url,
            quantidade: 1,
        });
    }

    localStorage.setItem(CHAVE, JSON.stringify(carrinho));
}

function mostrarToast(mensagem) {
    const toastAntigo = document.querySelector(".toast-carrinho");
    if (toastAntigo) toastAntigo.remove();

    const toast = document.createElement("div");
    toast.className = "toast-carrinho";
    toast.textContent = mensagem;
    document.body.appendChild(toast);

    requestAnimationFrame(() => toast.classList.add("toast-carrinho--visivel"));

    setTimeout(() => {
        toast.classList.remove("toast-carrinho--visivel");
        setTimeout(() => toast.remove(), 300);
    }, 2000);
}

function criarCard(produto) {
    const card = document.createElement("div");
    card.className = "card";
    card.setAttribute("role", "link");
    card.setAttribute("tabindex", "0");
    card.setAttribute("aria-label", `Ver detalhes de ${produto.nome || "produto"}`);

    card.innerHTML = `
        <div class="card__shine"></div>
        <div class="card__glow"></div>
        <div class="card__content">
            <div class="card__badge">Em estoque</div>
            <div class="card__image"></div>
            <div class="card__text">
                <h3 class="card__title"></h3>
                <p class="card__description"></p>
            </div>
            <div class="card__footer">
                <span class="card__price"></span>
                <button class="card__button" type="button" aria-label="Adicionar ao pedido">
                    ${ICONE_CARRINHO}
                </button>
            </div>
        </div>
    `;

    const imagemDiv = card.querySelector(".card__image");
    const tituloEl = card.querySelector(".card__title");
    const descEl = card.querySelector(".card__description");
    const precoEl = card.querySelector(".card__price");
    const badgeEl = card.querySelector(".card__badge");
    const botaoCarrinho = card.querySelector(".card__button");

    if (produto.imagem_url) {
        imagemDiv.style.backgroundImage = `url('${imagemUrlSegura(produto.imagem_url)}')`;
    }
    imagemDiv.setAttribute("role", "img");
    imagemDiv.setAttribute("aria-label", produto.nome || "Produto");

    tituloEl.textContent = produto.nome || "Produto sem nome";
    descEl.textContent = produto.descricao || "";
    precoEl.textContent = formatarPreco(produto.preco);

    const estoque = Number(produto.estoque);
    if (Number.isFinite(estoque) && estoque <= 0) {
        badgeEl.textContent = "Esgotado";
        badgeEl.style.background = "#dc2626";
    } else if (!Number.isFinite(estoque)) {
        badgeEl.remove();
    }

    // Clique no card inteiro -> vai pra página de detalhes do produto
    const irParaDetalhes = () => {
        window.location.href = `/produto/${produto.id_produto}`;
    };
    card.addEventListener("click", irParaDetalhes);
    card.addEventListener("keydown", (evento) => {
        if (evento.key === "Enter" || evento.key === " ") {
            evento.preventDefault();
            irParaDetalhes();
        }
    });

    // Botão do carrinho: adiciona rápido e NÃO navega para a página de detalhes
    botaoCarrinho.addEventListener("click", (evento) => {
        evento.stopPropagation();

        adicionarAoCarrinhoRapido(produto);
        renderizarCarrinho();
        atualizarResumo();

       mostrarToast(`${produto.nome} adicionado ao carrinho`);
    });

    return card;
}

function mostrarEstado(mensagemHtml) {
    container.innerHTML = `<div class="status-mensagem">${mensagemHtml}</div>`;
}

function mostrarErro() {
    mostrarEstado(`
        <strong>Não deu pra carregar o catálogo</strong>
        Verifique se o servidor Flask está rodando e tente de novo.
        <br>
        <button type="button" id="btn-tentar-novamente">Tentar novamente</button>
    `);
    document
        .getElementById("btn-tentar-novamente")
        .addEventListener("click", carregarProdutos);
}

function mostrarVazio() {
    mostrarEstado(`
        <strong>Nenhum produto cadastrado ainda</strong>
        Assim que produtos forem adicionados, eles aparecem aqui.
    `);
}

function criarListaCategorias(produtos) {
    if (!listaCategorias) return;

    const categorias = ["todos", ...new Set(
        produtos
            .map((produto) => String(produto.categoria || "").trim())
            .filter(Boolean)
            .sort((a, b) => a.localeCompare(b, "pt-BR"))
    )];

    listaCategorias.innerHTML = categorias
        .map((categoria) => {
            const nome = categoria === "todos" ? "Tudo" : categoria;
            const ativo = categoria === categoriaAtiva ? "ativo" : "";
            return `<li class="filtro-item ${ativo}" data-categoria="${categoria}">${nome}</li>`;
        })
        .join("");

    listaCategorias.querySelectorAll(".filtro-item").forEach((item) => {
        item.addEventListener("click", () => {
            categoriaAtiva = item.dataset.categoria;
            renderizarProdutos();
            listaCategorias.querySelectorAll(".filtro-item").forEach((botao) => {
                botao.classList.toggle("ativo", botao.dataset.categoria === categoriaAtiva);
            });
        });
    });
}

function renderizarProdutos() {
    if (!container) return;

    const produtosFiltrados = categoriaAtiva === "todos"
        ? produtosCarregados
        : produtosCarregados.filter((produto) => (produto.categoria || "") === categoriaAtiva);

    if (!produtosFiltrados.length) {
        mostrarVazio();
        if (contagemEl) contagemEl.textContent = "0 produtos";
        return;
    }

    container.innerHTML = "";
    produtosFiltrados.forEach((produto) => {
        container.appendChild(criarCard(produto));
    });

    if (contagemEl) {
        contagemEl.textContent = `${produtosFiltrados.length} produto${produtosFiltrados.length === 1 ? "" : "s"}`;
    }
}

async function carregarProdutos() {
    container.innerHTML = `
        <div class="skeleton"></div>
        <div class="skeleton"></div>
        <div class="skeleton"></div>
        <div class="skeleton"></div>
    `;

    try {
        const response = await fetch(ENDPOINT_PRODUTOS);
        if (!response.ok) {
            throw new Error(`Erro HTTP ${response.status}`);
        }
        const texto = await response.text();

        let resultado;
        try {
            resultado = JSON.parse(texto);
        } catch {
            throw new Error(`Erro do servidor: ${response.status}`);
        }

        if (!Array.isArray(resultado) || resultado.length === 0) {
            produtosCarregados = [];
            mostrarVazio();
            if (contagemEl) contagemEl.textContent = "0 produtos";
            return;
        }

        produtosCarregados = resultado;
        criarListaCategorias(resultado);
        renderizarProdutos();
    } catch (erro) {
        console.error("Falha ao carregar produtos:", erro);
        mostrarErro();
        if (contagemEl) contagemEl.textContent = "";
    }
}
function removerDoCarrinho(idProduto) {
    const CHAVE = "inovatech_carrinho";
    let carrinho = JSON.parse(localStorage.getItem(CHAVE)) || [];

    carrinho = carrinho.filter(item => item.id_produto !== idProduto);

    localStorage.setItem(CHAVE, JSON.stringify(carrinho));

    mostrarToast("Produto removido do carrinho");
    renderizarCarrinho();
    atualizarResumo();
}
function atualizarQuantidade(idProduto, novaQuantidade) {
    const CHAVE = "inovatech_carrinho";
    let carrinho = JSON.parse(localStorage.getItem(CHAVE)) || [];

    const item = carrinho.find(item => item.id_produto === idProduto);

    if (!item) return;
    
    const quantidade = Math.max(1, Number(novaQuantidade) || 1);
    item.quantidade = quantidade;

    localStorage.setItem(CHAVE, JSON.stringify(carrinho));

    renderizarCarrinho();
    atualizarResumo();
    }

function atualizarResumo() {
    const CHAVE = "inovatech_carrinho";
    let carrinho = JSON.parse(localStorage.getItem(CHAVE)) || [];
    
    // Calcular subtotal
    const subtotal = carrinho.reduce((total, item) => {
        return total + (item.preco * item.quantidade);
    }, 0);
    
    // Atualizar elementos HTML
    const subtotalEl = document.getElementById("subtotal");
    const totalEl = document.getElementById("total");
    const contagemEl = document.getElementById("contagem-itens");
    
    if (subtotalEl) {
        subtotalEl.textContent = formatarPreco(subtotal);
    }
    if (totalEl) {
        totalEl.textContent = formatarPreco(subtotal); // Sem desconto por enquanto
    }
    if (contagemEl) {
        const totalItens = carrinho.reduce((total, item) => total + item.quantidade, 0);
        contagemEl.textContent = totalItens;
    }
}
        
function renderizarCarrinho() {
    const CHAVE = "inovatech_carrinho";
    let carrinho = JSON.parse(localStorage.getItem(CHAVE)) || [];
    const listaCarrinho = document.getElementById("lista-carrinho");
    
    if (!listaCarrinho) return;
    
    if (carrinho.length === 0) {
        listaCarrinho.innerHTML = "<p>Seu carrinho está vazio</p>";
        return;
    }
    
    listaCarrinho.innerHTML = carrinho.map(item => `
        <div class="item-carrinho" data-produto-id="${item.id_produto}">
            <img src="${imagemUrlSegura(item.imagem_url)}" alt="${item.nome}">
            <div class="info-item">
                <h4>${item.nome}</h4>
                <p class="preco">${formatarPreco(item.preco)}</p>
            </div>
            <div class="quantidade">
                <button class="btn-menos" onclick="atualizarQuantidade(${item.id_produto}, ${item.quantidade - 1})">−</button>
                <input type="number" value="${item.quantidade}" min="1" 
                       onchange="atualizarQuantidade(${item.id_produto}, this.value)">
                <button class="btn-mais" onclick="atualizarQuantidade(${item.id_produto}, ${item.quantidade + 1})">+</button>
            </div>
            <div class="subtotal-item">${formatarPreco(item.preco * item.quantidade)}</div>
            <button class="btn-remover" onclick="removerDoCarrinho(${item.id_produto})">✕</button>
        </div>
    `).join("");
    
    atualizarResumo();
}

document.addEventListener("DOMContentLoaded", () => {
    if (document.getElementById("lista-carrinho")) {
        renderizarCarrinho();
    }
    // ... seu código existente
});

document.addEventListener("DOMContentLoaded", carregarProdutos);