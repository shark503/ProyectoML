$(document).ready(function() {

    $('#movieInput').autocomplete({
        source: function(request, response) {
            $.ajax({
                url: '/autocomplete',
                data: { q: request.term },
                success: function(data) {
                    response(data);
                }
            });
        },
        minLength: 2, 
    });
    
    $('#recommendBtn').click(function() {
        let movieName = $('#movieInput').val();
        if (!movieName) {
            $('#error-message').text('Ingrese el nombre de la pelicula');
            return;
        }
        $.ajax({
            type: 'POST',
            url: '/recommend',
            data: { movie: movieName },
            success: function(response) {
                let recommendations = $('#recommendations');
                let errorMessage = $('#error-message');
                recommendations.empty();
                errorMessage.text('');
                if (response.error) {
                    errorMessage.text(response.error);
                } else {
                    response.movies.forEach((movie, index) => {
                        let movieCard = `
                            <div class="card" style="width: 18rem;">
                                <img src="${response.posters[index]}" class="card-img-top" alt="${movie}">
                                <div class="card-body">
                                    <h5 class="card-title">${movie}</h5>
                                </div>
                            </div>`;
                        recommendations.append(movieCard);
                    });
                }
            }
        });
    });
});
