function toggleDivVisibility(checkbox, divId) {
    const div = document.getElementById(divId);
    if (checkbox.checked) {
        div.style.display = "block";
    } else {
        div.style.display = "none";
    }
}
    
function toggleEleRequired(checkbox, eleId) {
    const ele = document.getElementById(eleId);
    if (checkbox.checked) {
        ele.required = true;
    } else {
        ele.required = false;
    }
}

