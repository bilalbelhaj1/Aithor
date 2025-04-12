// Dashboard: User Growth Chart
const ctxUserGrowth = document.getElementById('userGrowthChart').getContext('2d');
const userGrowthChart = new Chart(ctxUserGrowth, {
    type: 'line',
    data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
        datasets: [{
            label: 'User Growth',
            data: [50, 100, 150, 200, 250],
            borderColor: '#32CD32', // Lime Green
            fill: false,
            tension: 0.1
        }]
    }
});

// Analysis: Stories Generated Chart
const ctxStoriesGenerated = document.getElementById('storiesGeneratedChart').getContext('2d');
const storiesGeneratedChart = new Chart(ctxStoriesGenerated, {
    type: 'bar',
    data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
        datasets: [{
            label: 'Stories Generated',
            data: [50, 80, 100, 120, 150],
            backgroundColor: '#98fb98', // Pale Green
            borderColor: '#2f4f4f',
            borderWidth: 1
        }]
    }
});

// Analysis: Saved Stories Chart
const ctxSavedStories = document.getElementById('savedStoriesChart').getContext('2d');
const savedStoriesChart = new Chart(ctxSavedStories, {
    type: 'pie',
    data: {
        labels: ['Saved', 'Not Saved'],
        datasets: [{
            data: [60, 40],
            backgroundColor: ['#3a5a40', '#ff6347']
        }]
    }
});
