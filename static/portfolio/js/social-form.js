function openForm(social_network) {
    document.getElementById("socialModal").style.display = "flex";
    document.getElementById(social_network).value = social_network;
}

function closeForm() {
    document.getElementById("socialModal").style.display = "none";
}