# First RESTful API

#### 9th Oct 2025

### What?

On 9th of October, I developed a solid foundation to what will become my personal website. The website features a REST compliant API, a frontend, database integration, version control, and 3 endpoints; `/projects`, `/about`, `feedback`.

### So what?

Going into this project, I had no prior knowledge of REST, and a very limited experience with Flask. I didn't know what REST was about, and trying to educate myself with online resources proved quite a challenge. Everything was confusing and solid understanding seemed to have required a comprehensive knowledge of how websites work and communicate. 

Struggling to comprehend the task, I decided to go in head first, and started to develop the application, and consequently fell into many pitfalls, such as:

* I developed the headed version first, thinking that the API was only supposed to be accessed via frontend.

* Built ununiform endpoints for data manipulation (`/projects/edit`, `/projects/delete` as opposed to `/projects/<int:project_ID>`), thinking I was doing so in accordance with REST's requirements.

But it is thanks to those mistakes I made that I was able to understand what was being asked of me. Once I had developed the frontend, with what I had, I dove deep into research, and listed all of the things that I was doing wrong, and transformed the unknown unknowns into known unknowns. Then it clicked, and it snowballed from there,

I researched concenpts such as Multimedia Internet Mail Exchange (MIME), Hypermedia as the Engine of the Application State (HATEOAS), different headers such as `Accept-` or `Cache-Control`, Unique Resource Identifier (URI), and different HTTP statuses.

With the newly gained knowledge, the requirements of REpresentational State Transfer (REST) became much clearer, and I was able to start working away at the issues I had listed.

Couple hours of intense focus later, I had a fully RESTful API on my hands,

* JSON representations of site resources were being transferred,

* Every endpoint explicitly imposed allowed methods,

* Every endpoint returned at least two status codes,

* All requests for the same resource had the same URI ,

* The server was completely independent of the client and vice versa,

* Every response included explicit information about caching permissions,

* Neither the server nor the client had to be aware of whether they're communicating with the end application or an intermediary,

* The JSON responses included URLs to further actions to allow manipulation of resources without the knowledge of the website's architecture.

### Now what?

Now that the application is well outlined, and the assignment for it submitted, I will carry on tinkering with it until it's good enough to show to show to other people. I will add more endpoints, improve frontend, and integrate the API into my other applications such as my electronic journal, or GitHub pipelines. 

I'm planning on making this application my professional website meant for advertisement, promotion, and showcasing of my abilities as a software developer and more.
