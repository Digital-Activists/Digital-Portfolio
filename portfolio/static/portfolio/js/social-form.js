function openForm(social_network) {
    document.getElementById("socialModal").style.display = "flex";
    document.getElementById("social-network-hidden-input").value = social_network;
    if (social_network in social_networks_dict){
        document.getElementById("social-network-input").value = social_networks_dict[social_network];
    }
}

function closeForm() {
    document.getElementById("socialModal").style.display = "none";
    document.getElementById("social-network-hidden-input").value = "";
    document.getElementById("social-network-input").value = "";
}

