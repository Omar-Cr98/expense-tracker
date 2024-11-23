document.getElementById('expense-form').addEventListener('submit', async function (e) {
    e.preventDefault(); // Prevent form submission

    const formData = {
        ID: document.getElementById('id').value,
        Item_ID: document.getElementById('item-id').value,
        Item_Name: document.getElementById('item-name').value,
        Item_Type: document.getElementById('item-type').value,
        Amount: parseFloat(document.getElementById('amount').value),
        Pay_DATE: document.getElementById('pay-date').value,
        Who_Payed: document.getElementById('who-payed').value
    };

    try {
        const response = await fetch('/add-expense', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        const result = await response.json();
        const messageDiv = document.getElementById('message');
        if (response.ok) {
            messageDiv.textContent = result.message;
            messageDiv.style.color = 'green';
        } else {
            messageDiv.textContent = result.error;
            messageDiv.style.color = 'red';
        }
    } catch (error) {
        console.error('Error:', error);
    }
});
