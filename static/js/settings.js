const sidebar = document.querySelector('.sidebar');
const sidebarIcon = document.querySelector('.sidebar-icon');
const closeBtn = document.querySelector('.close-btn');

sidebarIcon.addEventListener('click', () => {
    sidebar.classList.toggle('show');
});

closeBtn.addEventListener('click', () => {
    sidebar.classList.remove('show');
});

function changePassword() {
  var confirmacao = confirm("Deseja realmente alterar sua senha?")
  if(confirmacao === false) {
    return alert("Ok, operação cancelada.")
  } else {
    var senha = prompt("Certo, agora digite sua senha atual")
    
    var novaSenha = prompt("Agora, digite uma nova senha")
    
    axios.post("/api/edit-password", {
      "password": senha,
      "passwordNew": novaSenha,
      "user": localStorage.getItem("username")
    }).then((r) => {
      var msg = r.data.message 
      if(msg === "success") {
        return alert("Senha alterada com sucesso!")
      } else {
        return alert("Senha incorreta!!")
      }
    })
  }
}

function changeUsername() {
  var confirmacao = confirm("Deseja realmente mudar seu nome de usuário?")
  if(confirmacao === true) {
    var senha = prompt("Ok, agora digite sua senha")
    var newUsername = prompt("Digite seu novo nome de usuário")
    
    axios.post("/api/edit-username", {
      "user": localStorage.getItem("username"),
      "usernameNew": newUsername,
      "password": senha
    }).then((r) => {
      var msg = r.data.message 
      if(msg === "success") {
        localStorage.setItem("username", newUsername)
        return alert("Nome de usuário alterado com sucesso para: " + newUsername)
      } if(msg === "incorrect password") {
        return alert("Senha incorreta!!")
      } else {
        return alert("Ocorreu um erro ao alterar o nome de usuário, talvez você tenha digitado o mesmo nome de usuário atual.")
      }
    })
  }
                            }

function ApagarConta() {
    axios.post(`/api/delete`, {
        "user": localStorage.getItem('username')
    })
  localStorage.removeItem("username")
  window.location.href = "/cadastro"
}

function Sair() {
    localStorage.removeItem('username')
    localStorage.removeItem('coins')
    window.location.href = '/conectar'
}

document.querySelector('.coins > span').innerHTML = localStorage.getItem('coins')