function CriarTarefa() {
    var nomeTarefa = $('#name-task').val()
    var descricaoTarefa = $('#description-task').val()
    var dataConclusao = document.querySelector("#conclusao").value
    if(!dataConclusao) {
      dataConclusao = new Date().toISOString().substr(0, 10); 

}
    var es = dataConclusao.split("-")
    dataConclusao = `${es[2]}/${es[1]}/${es[0]}`

    const dataTask = {
        "name": nomeTarefa,
        "description": descricaoTarefa,
        "conclusion": dataConclusao,
        'user': localStorage.getItem('username')
    }

    console.log(dataTask)
    axios.post('/api/create-task', dataTask).then((r) => {
        var resposta = r.data.response 

        if(resposta === "Preciso de nome e descrição válido") {
            return alert('Digite um nome e descrição válido')
        } else {
            return alert('Tarefa adicionada com sucesso')
        }
    })
}
// Verifica se já tem usuário logado
if(!localStorage.getItem("username")) { 
   window.location.href = "/cadastro"
}

document.querySelector('.coins > span').innerHTML = localStorage.getItem('coins')

const data = []

// Pega as tasks do usuário

axios.get(`/api/tasks/${localStorage.getItem('username')}`).then((r) => {
  
    var resposta = r.data.message
    var days = r.data.days 
    days.forEach(element => {
      document.querySelector(".days").innerHTML += element
    })
    resposta.forEach(element => {
      data.push({
        name: element.name,
        description: element.description,
        status: element.status,
        check: false
      })

      if(element.status === "concluido") {
        const taski = data.find((obj) => obj.name == element.name)
        taski.check = true
}

if(element.status === "pendente") {        document.querySelector('.list').innerHTML += `
                <div data-name="${element.name}" data-description="${element.description}" data-prazo="${element.conclusion}" class="task">
        <input type="checkbox" data-name="${element.name}" id="check-task">
        <div class="infos">
            <p class="task-name" data-name="${element.name}" data-description="${element.description}" data-prazo="${element.conclusion}" ><strong>${element.name}</strong></p>
            <i data-name="${element.name}" data-prazo="${element.conclusion}" data-description="${element.description}" class="icon fas fa-trash delete"></i>
        </div>
    </div>
        `
      } else {
         document.querySelector('.list').innerHTML += `
        <div data-name="${element.name}" data-description="${element.description}" data-prazo="${element.conclusion}" class="task">
        <input type="checkbox" data-name="${element.name}" id="check-task" checked>
        <div class="infos">
            <p class="task-name" data-name="${element.name}" data-description="${element.description}" data-prazo="${element.conclusion}" ><strong>${element.name}</strong></p>
            <i data-name="${element.name}" data-prazo="${element.conclusion}" data-description="${element.description}" class="icon fas fa-trash delete"></i>
        </div>
    </div>
        `
      }
    });
    
    // Seleciona todos os checkboxes
const checkboxes = document.querySelectorAll('#check-task');

// Itera sobre cada checkbox
checkboxes.forEach((checkbox) => {
  // Adiciona um evento de clique a cada checkbox
  checkbox.addEventListener('click', () => {
    // Pega o valor do atributo data-id do checkbox clicado
    const id = checkbox.getAttribute('data-name');
    console.log(`Checkbox com id ${id} clicado`);
    const status = checkbox.getAttribute("data-status")
    const task = data.find((obj) => obj.name === id)

    task.check = true

    axios.post(`/api/concluir-task`, {
        'user': localStorage.getItem('username'),
        'name': task.name,
        'description': task.description,

      "coin": parseInt(localStorage.getItem("coins"))
    }).then((r) => {
        const resposta = r.data.message
        alert(resposta.status)
        if(resposta.status.includes('ganhou')) {
            
            localStorage.setItem('coins', parseInt(localStorage.getItem('coins')) + 10)
            document.querySelector('.coins > span').innerHTML = localStorage.getItem('coins')
        } if (resposta.status.includes('ganhou')) {
  localStorage.setItem('coins', parseInt(localStorage.getItem('coins')) + 10);
  document.querySelector('.coins > span').innerHTML = localStorage.getItem('coins');
} else if (resposta.status.includes("dentro")) {
  localStorage.setItem('coins', parseInt(localStorage.getItem('coins')) + 5);
} else {
  localStorage.setItem('coins', parseInt(localStorage.getItem('coins')) - 10);
}
           })
    })
  });
  document.querySelectorAll(".task-name").forEach((taskHtml) => {
  taskHtml.addEventListener('click', function(e) {
    var title = taskHtml.getAttribute("data-name")
    var description = taskHtml.getAttribute("data-description")
    var prazo = taskHtml.getAttribute("data-prazo")
    
    alert(`
      Nome da tarefa: ${title}
      Descrição: ${description}
      Prazo: ${prazo}
    `)
    
  })
})

document.querySelectorAll(".infos > i").forEach((element) => {
  element.addEventListener('click', function () {
    var nome = element.getAttribute("data-name")
    var description = element.getAttribute("data-description")
    
    axios.post("/api/delete-task", {
      "name": nome,
      "description": description,
      "user": localStorage.getItem("username")
    }).then((r) => {
      var res = r.data.message.message
      if(res === "Tarefa excluída com sucesso!") {
        return alert("Tarefa excluída com sucesso")
      } else {
        return alert("Erro ao excluir a tarefa")
      }
    })
  })
})
});

          

console.log(data)

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

function deleteAllTask() {
  axios.post("/api/delete/all", {
    "autor": localStorage.getItem("username")
  }).then((r) => {
    var resposta = r.data.message 
    if(resposta === "sucesso") {
      return alert("Tarefas Excluídas com sucesso!")
    } else {
      return alert("Erro ao excluir tarefas, tente novamente mais tarde")
    }
  })
}

const sidebar = document.querySelector('.sidebar');
const sidebarIcon = document.querySelector('.sidebar-icon');
const closeBtn = document.querySelector('.close-btn');

sidebarIcon.addEventListener('click', () => {
    sidebar.classList.toggle('show');
});

closeBtn.addEventListener('click', () => {
    sidebar.classList.remove('show');
});

