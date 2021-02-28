<h1> Dmon REST API </h1>

<p> This is a REST API service for Dmon game. You can try it live on <a href="https://dmon-api.herokuapp.com/">https://dmon-api.herokuapp.com/</a></p>


<h2> Usage </h2>

<p>You can see documentation of API in both <a href="https://dmon-api.herokuapp.com/docs">swagger</a> and <a href="https://dmon-api.herokuapp.com/redoc">redoc</a> style.</p>

<h3> How to use it? </h3>


<ul>
    <li>Create a new user account by <strong>POST</strong> request to <code>/users</code> endpoint.</li>
    <li>Create new token by <strong>POST</strong> request to <code>/token</code> endpoint.</li>
    <li>You can create new user by <strong>POST</strong> request to <code>/users</code> endpoint.</li>
    <li>You can get info about current user by <strong>GET</strong> request to <code>/users/me</code> endpoint.</li>
    <li>You can view all tokens created on blockchain by <strong>GET</strong> request to <code>/item/{item_id}</code> endpoint.</li>
    <li>You can view all monsters owned by current user by <strong>GET</strong> request to <code>/monsters</code> endpoint.</li>
</ul>
