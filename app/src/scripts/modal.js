function openModal(modalName) {
    const modal = document.getElementById(modalName);
    modal.style.display = 'flex';
    // Trigger reflow to ensure transition works
    modal.offsetHeight;
    modal.style.transform = 'translateX(100%)';
}

function closeModal(modalName) {
    const modal = document.getElementById(modalName);
    modal.style.display = 'none';
}
