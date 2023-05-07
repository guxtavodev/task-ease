function Cadastrar() {
    var nome = $('#username').val()
    var senha = $('#password').val()

    axios.post(`/api/cadastro`, {
        "username": nome,
        "password": senha
    }).then((response) => {
        var resposta = response.data.response.message
        console.log(response.data)
        if(resposta === "Já existe usuário com este nome") {
            return alert("Este nome de usuário não está disponível, tente outro.")
        } if(resposta === "Usuário cadastrado com sucesso!") {
            localStorage.setItem('username', nome)
            localStorage.setItem('coins', response.data.response.coins)
            return window.location.href = "/home"
        }
    })
}

if(localStorage.getItem("username")
) {
   window.location.href = "/home"
}