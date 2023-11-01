var clipboard = new ClipboardJS("#copy_emails", {
    text: function () {
        // Получаем значение email из элемента input
        var emailInput = document.getElementById("id_email");
        return emailInput.value;
    }
});

// Отслеживаем успешное копирование
clipboard.on("success", function (e) {
    alert("Email copied to clipboard: " + e.text);
    e.clearSelection();
});

// Отслеживаем ошибку при копировании
clipboard.on("error", function (e) {
    alert("Error copying email. Please copy manually.");
});