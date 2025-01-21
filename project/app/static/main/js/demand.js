// График: Динамика уровня зарплат по годам
const salaryByYearCtx = document.getElementById('salaryByYearChart').getContext('2d');
const salaryLabels = JSON.parse(document.getElementById('salaryLabels').textContent);
const salaryData = JSON.parse(document.getElementById('salaryData').textContent);

const salaryByYearChart = new Chart(salaryByYearCtx, {
    type: 'line',
    data: {
        labels: salaryLabels,
        datasets: [{
            label: 'Средняя З/П (руб.)',
            data: salaryData,
            backgroundColor: 'rgba(54, 162, 235, 0.5)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

// График: Динамика количества вакансий по годам
const vacanciesByYearCtx = document.getElementById('vacanciesByYearChart').getContext('2d');
const vacancyLabels = JSON.parse(document.getElementById('vacancyLabels').textContent);
const vacancyData = JSON.parse(document.getElementById('vacancyData').textContent);

const vacanciesByYearChart = new Chart(vacanciesByYearCtx, {
    type: 'bar',
    data: {
        labels: vacancyLabels,
        datasets: [{
            label: 'Количество вакансий',
            data: vacancyData,
            backgroundColor: 'rgba(255, 99, 132, 0.5)',
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});
