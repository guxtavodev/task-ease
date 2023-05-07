function Entrar() {
    var nome = $('#username').val()
    var senha = $('#password').val()

    axios.get(`/api/auth?username=${nome}&password=${senha}`).then((res) => {
        var resposta = res.data.response.message 
        if(resposta === "Usuário não existe") {
            return alert('Não existe nenhum usuário com este nome1')
        } if(resposta === "Senha incorreta") {
            return alert("Senha incorreta! Tente novamente")
        } if(resposta === "Senha correta") {
            localStorage.setItem('username', nome)
            localStorage.setItem('coins', res.data.response.coins)
            return window.location.href = "/home"
        }
    })
}