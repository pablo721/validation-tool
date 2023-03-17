function addAttribute(){

    function delRow(){
        row.remove();
    }

    var form = document.getElementById('new_process_form');
    var table = document.getElementById('new_process_attrs_table');
    var row = table.insertRow();
    var n_row = (table.rows.length - 1).toString();

    var input = document.createElement('input');
    input.id = 'new_process_attr_name_input';
    input.name = 'attribute_name_' + n_row;
    input.type = 'text';
    input.placeholder = 'Attribute name';
    var td = row.insertCell();
    td.appendChild(input);

    var select = document.createElement('select');
    select.id = 'new_process_select';
    select.name = 'dtype_' + n_row;
    select.className = 'cls-attr-input';
    var options = ['str','int','float','date'];

    for (var item of options){
        var opt = document.createElement('option');
        opt.text = item;
        opt.name = 'dtype_option';
        opt.value = item;
        select.appendChild(opt);
    }
    var td2 = row.insertCell();
    td2.appendChild(select);


    var max_size_input = document.createElement('input');
    max_size_input.type = 'text';
    max_size_input.label = 'Max size';
    max_size_input.name = 'max_size_' + n_row;
    var td22 = row.insertCell();
    td22.appendChild(max_size_input);


    var checkbox_required = document.createElement('input');
    checkbox_required.type = 'checkbox';
    checkbox_required.label = 'Required';
    checkbox_required.name = 'required_' + n_row;
    var td3 = row.insertCell();
    td3.appendChild(checkbox_required);

    var checkbox_unique = document.createElement('input');
    checkbox_unique.type = 'checkbox';
    checkbox_unique.label = 'Unique';
    checkbox_unique.name = 'unique_' + n_row;
    var td4 = row.insertCell();
    td4.appendChild(checkbox_unique);

    var checkbox_unique_together = document.createElement('input');
    checkbox_unique_together.type = 'checkbox';
    checkbox_unique_together.label = 'Unique together';
    checkbox_unique_together.name = 'unique_together_' + n_row;
    var td5 = row.insertCell();
    td5.appendChild(checkbox_unique_together);



    var btn = document.createElement('input');
    btn.id = 'new_process_del_btn';
    btn.name = 'new_process_del_btn';
    btn.className = 'cls-attr-input';
    btn.type = 'button';
    btn.value = '-';
    btn.addEventListener('click', delRow, false);
    var td6 = row.insertCell();
    td6.appendChild(btn);


}

function addAttribute2(){
    var form = document.getElementById('new_process_form');
    var div = document.createElement('div');
    div.className = 'cls-attr-div';
    console.log(div);
    console.log(div.className);
    function delRow(){
        div.remove();
    }


    var input = document.createElement('input');
    input.id = 'new_process_attr_name_input';
    input.name = 'new_process_attr_name_input';
    input.type = 'text';
    input.className = 'cls-attr-input';
    input.placeholder = 'Attribute name';
    div.appendChild(input);

    var select = document.createElement('select');
    select.id = 'new_process_select';
    select.name = 'new_process_select';
    select.className = 'cls-attr-input';
    var options = ['string','int','float','date'];

    for (var item of options){
        console.log(item);
        var opt = document.createElement('option');

        opt.text = item;
        opt.name = 'dtype_option';
        opt.value = item;
        console.log(opt);
        select.appendChild(opt);
    }
    div.appendChild(select);

    var checkbox_null = document.createElement('input');
    checkbox_null.type = 'checkbox';
    checkbox_null.label = 'Nullable';
    checkbox_null.name = 'nullable';
    div.appendChild(checkbox_null);

    var checkbox_unique = document.createElement('input');
    checkbox_unique.type = 'checkbox';
    checkbox_unique.label = 'Unique';
    checkbox_unique.name = 'unique';
    div.appendChild(checkbox_unique);

    var checkbox_unique_together = document.createElement('input');
    checkbox_unique.type = 'checkbox';
    checkbox_unique.label = 'Unique together';
    checkbox_unique.name = 'unique_together';
    div.appendChild(checkbox_unique_together);



    var btn = document.createElement('input');
    btn.id = 'new_process_del_btn';
    btn.name = 'new_process_del_btn';
    btn.className = 'cls-attr-input';
    btn.type = 'button';
    btn.value = '-';
    btn.addEventListener('click', delRow, false);
    div.appendChild(btn);



    form.appendChild(div);

}