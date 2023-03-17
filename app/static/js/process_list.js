

function filterProcesses(){
    var text = document.getElementById('index_text_input').value.toLowerCase();
    var process_list = document.getElementById('index_process_list');

    if (!text) {
        for (var item of process_list.children){
            item.style.display = 'list-item';
            }
    }

    for (var item of process_list.children){
        var txt = item.innerText;
        console.log(txt);
        if (!txt.toString().includes(text)){
            item.style.display = 'none';
        }

    }
}

