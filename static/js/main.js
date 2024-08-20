// code is wrapped in an IIFE (Immediately Invoked Function Expression). See https://developer.mozilla.org/en-US/docs/Glossary/IIFE for more details
//
(() => {
  // globals
  restApiURL = '/api/';
  data = null;

  async function loadData(){ 
    try{
        //after this line, our function will wait for the `fetch()` call to be settled
        //the `fetch()` call will either return a Response or throw an error
        const response = await fetch(restApiURL);
        if(!response.ok){
            throw new Error(`HTTPerror:${response.status}`);
        }
        //after this line, our function will wait for the`response.json()`call to be settled
        //the`response.json()`call will either return the parsed JSON object or throw an error 
        data=await response.json();
        console.log(data);
        render(); // update the DOM
    } catch(error){
        console.error(`Could not get product data:${error}`);
    }
  }

  function render() {
    blogPostContainer = document.querySelector('.container.blog-posts');

    let outputHtml = '<ul>';
    data.forEach((blogPost) => {
      outputHtml += `<li><a href="${restApiURL}/${blogPost.id}">${blogPost.title} by ${blogPost.author}</a></li>`;
    });  
    outputHtml += '</ul>';
    
    blogPostContainer.innerHTML = outputHtml;
  }

  function init() {
    console.info("DOM loaded");
    loadData();
  }
  
  if (document.readyState === "loading") {
    // Loading hasn't finished yet
    document.addEventListener("DOMContentLoaded", init);
  } else {
    // `DOMContentLoaded` has already fired
    init();
  }

})();  