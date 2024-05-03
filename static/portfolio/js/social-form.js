function openForm(social_network) {
    document.getElementById("socialModal").style.display = "flex";
    document.getElementById("social-network-hidden-input").value = social_network;
}

function closeForm() {
    document.getElementById("socialModal").style.display = "none";
    document.getElementById("social-network-hidden-input").value = "";
}