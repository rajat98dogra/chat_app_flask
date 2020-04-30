document.addEventListener('DOMContentLoaded', () => {
var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
let room="Game";
joinRoom('Game')

    socket.on('message' ,data=>{


    const p=document.createElement('p')
    document.querySelector('#display-section').innerHTML=`${data.mes}`

    });

    socket.on('announce' ,data=>{
    console.log(data.mes,"$$")

    let v=document.querySelectorAll('#list>p')
    if(v.length > 5){
    var list = document.getElementById("list");
    list.removeChild(list.childNodes[0]);
    }
    const div=document.createElement('p')

    div.innerHTML= `Channel ${data['room']} User[${data['user']}] => ${data['mes']}</p>`

    document.querySelector('#list').append(div)
    })
     document.getElementById('send_message').onclick=()=>{
    const mes =document.getElementById("mes").value;
    console.log(mes,"###",username)
    socket.emit('submit',{'name':username,'mes':mes,'room':room});

    }

    document.querySelectorAll('.select-room').forEach( p=>{
    p.onclick =()=>{
    let newRoom =p.innerHTML
    console.log(newRoom)
    if(newRoom==room){
        msg=`already in ${room} room`;
        printmsg(msg)
    }
    else{
        leaveRoom(room)
        joinRoom(newRoom)
        room=newRoom
    }
    }

    });


    socket.on('room',data=> {
    var el=document.querySelector('#list')
    el.innerHTML=data['mes']
     document.querySelector('#list').append(el)
    })

    function printmsg(msg){
    document.querySelector('#display-section').innerHTML=msg
    }

    function leaveRoom(room){
    socket.emit('leave',{'username':username,'room':room})
    }

    function joinRoom(room){
    socket.emit('join',{'username':username,'room':room})
    socket.emit('cache',{'username':username,'room':room})
    document.querySelector('#display-section').innerHTML=''
    document.querySelector("#mes").focus()
    }

    socket.on('memory',data=>{
    console.log('memory')
    document.querySelector('#list').innerHTML=''
    for(let i=0 ;i<data['cache'].length;i++){
    var c=data['cache'][i]
    mes=c['mes']
    user=c['user']
    room=c['room']
    const p=document.createElement('p')

    p.innerHTML= `Channel ${room} User[${user}] => ${mes}</p>`

    document.querySelector('#list').append(p)

    }
    })
    })
