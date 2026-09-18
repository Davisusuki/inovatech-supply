const formCliente = document.getElementById("form-cliente");
const listaClientes = document.getElementById("lista-clientes");
const buscaCliente = document.getElementById("busca-cliente");
const contagemClientes = document.getElementById("contagem-clientes");
const mensagemFormulario = document.getElementById("mensagem-formulario");
const clienteId = document.getElementById("cliente-id");
const btnSalvar = document.getElementById("btn-salvar");
const btnCancelar = document.getElementById("btn-cancelar");

let clientes = [];

function escaparHtml(valor) {
    return String(valor || "").replace(/[&<>'"]/g, (caractere) => ({
        "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;"
    })[caractere]);
}

function mostrarMensagem(texto, erro = false) {
    mensagemFormulario.textContent = texto;
    mensagemFormulario.classList.toggle("mensagem-erro", erro);
}

function renderizarClientes() {
    const termo = buscaCliente.value.trim().toLocaleLowerCase("pt-BR");
    const filtrados = clientes.filter((cliente) =>
        [cliente.nome, cliente.nome_empresa, cliente.email].some((campo) =>
            String(campo || "").toLocaleLowerCase("pt-BR").includes(termo)
        )
    );
    contagemClientes.textContent = `${clientes.length} cliente${clientes.length === 1 ? "" : "s"}`;
    if (!filtrados.length) {
        listaClientes.innerHTML = `<p class="estado-clientes">${clientes.length ? "Nenhum cliente encontrado." : "Nenhum cliente cadastrado ainda."}</p>`;
        return;
    }
    listaClientes.innerHTML = filtrados.map((cliente) => `
        <article class="cliente-linha">
            <div class="cliente-avatar">${escaparHtml(cliente.nome).charAt(0).toUpperCase()}</div>
            <div class="cliente-dados">
                <h3>${escaparHtml(cliente.nome)}</h3>
                <p>${escaparHtml(cliente.nome_empresa || "Pessoa física")}</p>
                <small>${escaparHtml(cliente.email || "Sem e-mail")} ${cliente.telefone ? `· ${escaparHtml(cliente.telefone)}` : ""}</small>
            </div>
            <div class="cliente-acoes">
                <button type="button" class="btn-icone" data-editar="${cliente.id_cliente}">Editar</button>
                <button type="button" class="btn-icone btn-excluir" data-excluir="${cliente.id_cliente}">Excluir</button>
            </div>
        </article>
    `).join("");
}

async function carregarClientes() {
    try {
        const resposta = await fetch("/clientes/");
        if (!resposta.ok) throw new Error("Não foi possível carregar os clientes.");
        clientes = await resposta.json();
        renderizarClientes();
    } catch (erro) {
        listaClientes.innerHTML = `<p class="estado-clientes mensagem-erro">${erro.message}</p>`;
    }
}

function preencherFormulario(cliente) {
    clienteId.value = cliente.id_cliente;
    ["nome", "nome_empresa", "pais", "email", "telefone"].forEach((campo) => {
        document.getElementById(campo).value = cliente[campo] || "";
    });
    document.getElementById("titulo-formulario").textContent = "Editar cliente";
    btnSalvar.textContent = "Salvar alterações";
    btnCancelar.hidden = false;
    document.getElementById("nome").focus();
}

function limparFormulario() {
    formCliente.reset();
    clienteId.value = "";
    document.getElementById("pais").value = "Brasil";
    document.getElementById("titulo-formulario").textContent = "Novo cliente";
    btnSalvar.textContent = "Cadastrar cliente";
    btnCancelar.hidden = true;
    mostrarMensagem("");
}

formCliente.addEventListener("submit", async (evento) => {
    evento.preventDefault();
    const dados = Object.fromEntries(new FormData(formCliente));
    delete dados["cliente-id"];
    const id = clienteId.value;
    btnSalvar.disabled = true;
    try {
        const resposta = await fetch(id ? `/clientes/${id}` : "/clientes/", {
            method: id ? "PUT" : "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(dados)
        });
        const resultado = await resposta.json();
        if (!resposta.ok) throw new Error(resultado.erro || "Não foi possível salvar o cliente.");
        limparFormulario();
        await carregarClientes();
        mostrarMensagem(id ? "Cliente atualizado com sucesso." : "Cliente cadastrado com sucesso.");
    } catch (erro) {
        mostrarMensagem(erro.message, true);
    } finally {
        btnSalvar.disabled = false;
    }
});

listaClientes.addEventListener("click", async (evento) => {
    const editar = evento.target.closest("[data-editar]");
    const excluir = evento.target.closest("[data-excluir]");
    if (editar) preencherFormulario(clientes.find((cliente) => cliente.id_cliente === Number(editar.dataset.editar)));
    if (excluir && confirm("Excluir este cliente?")) {
        const resposta = await fetch(`/clientes/${excluir.dataset.excluir}`, { method: "DELETE" });
        if (resposta.ok) carregarClientes();
    }
});

buscaCliente.addEventListener("input", renderizarClientes);
btnCancelar.addEventListener("click", limparFormulario);
carregarClientes();
