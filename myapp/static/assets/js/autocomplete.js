function autocomplete(inp, arr) {
    /*the autocomplete function takes two arguments,
    the text field element and an array of possible autocompleted values:*/
    var currentFocus;
    /*execute a function when someone writes in the text field:*/
    inp.addEventListener("input", function(e) {
      var a, b, i, val = this.value;
      
      /* ### Nicht umgesetzte Funktion ###
      ### 403 Forbidden (CSRF token missing. ### 

      var search_game = "default"
      // search_term = document.getElementById("gameName").firstElementChild.value;

      // window.location.href = "{% url 'igdb_api_search_game_search/' search_term = " + search_term + "  % }"

      var formData = new FormData();
      formData.append('search_game', search_game)
      formData.append('csrfmiddlewaretoken', "{{ csrf_token }}")

      $.ajax({
        url: "api-call-search-game",
        method: "POST",
        processData: false,
        contentType: false,
        data: formData,
        mimeType: 'data/text',
        success: function(data) {
          window.location.href = "/app"
        }
      })/*

        /*close any already open lists of autocompleted values*/
        closeAllLists();
        if (!val) { return false;}
        currentFocus = -1;
        /*create a DIV element that will contain the items (values):*/
        a = document.createElement("DIV");
        a.setAttribute("id", document.getElementById("gameName") + "autocomplete-list");
        a.setAttribute("class", "autocomplete-items");
        /*append the DIV element as a child of the autocomplete container:*/
        document.getElementById("gameName").appendChild(a);
        /*for each item in the array...*/
        for (i = 0; i < arr.length; i++) {
          /*check if the item starts with the same letters as the text field value:*/
          if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
            /*create a DIV element for each matching element:*/
            b = document.createElement("DIV");
            /*make the matching letters bold:*/
            b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
            b.innerHTML += arr[i].substr(val.length);
            /*insert a input field that will hold the current array item's value:*/
            b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
            /*execute a function when someone clicks on the item value (DIV element):*/
            b.addEventListener("click", function(e) {
                /*insert the value for the autocomplete text field:*/
                inp.value = this.getElementsByTagName("input")[0].value;
                /*close the list of autocompleted values,
                (or any other open lists of autocompleted values:*/
                closeAllLists();
            });
            a.appendChild(b);
          }
        }
    });
    /*execute a function presses a key on the keyboard:*/
    inp.addEventListener("keydown", function(e) {
        var x = document.getElementById(document.getElementById("gameName") + "autocomplete-list");
        if (x) x = x.getElementsByTagName("div");
        if (e.keyCode == 40) {
          /*If the arrow DOWN key is pressed,
          increase the currentFocus variable:*/
          currentFocus++;
          /*and and make the current item more visible:*/
          addActive(x);
        } else if (e.keyCode == 38) { //up
          /*If the arrow UP key is pressed,
          decrease the currentFocus variable:*/
          currentFocus--;
          /*and and make the current item more visible:*/
          addActive(x);
        } else if (e.keyCode == 13) {
          /*If the ENTER key is pressed, prevent the form from being submitted,*/
          e.preventDefault();
          if (currentFocus > -1) {
            /*and simulate a click on the "active" item:*/
            if (x) x[currentFocus].click();
          }
        }
    });
    function addActive(x) {
      /*a function to classify an item as "active":*/
      if (!x) return false;
      /*start by removing the "active" class on all items:*/
      removeActive(x);
      if (currentFocus >= x.length) currentFocus = 0;
      if (currentFocus < 0) currentFocus = (x.length - 1);
      /*add class "autocomplete-active":*/
      x[currentFocus].classList.add("autocomplete-active");
    }
    function removeActive(x) {
      /*a function to remove the "active" class from all autocomplete items:*/
      for (var i = 0; i < x.length; i++) {
        x[i].classList.remove("autocomplete-active");
      }
    }
    function closeAllLists(elmnt) {
      /*close all autocomplete lists in the document,
      except the one passed as an argument:*/
      var x = document.getElementsByClassName("autocomplete-items");
      for (var i = 0; i < x.length; i++) {
        if (elmnt != x[i] && elmnt != inp) {
          x[i].parentNode.removeChild(x[i]);
        }
      }
    }
    /*execute a function when someone clicks in the document:*/
    document.addEventListener("click", function (e) {
        closeAllLists(e.target);
    });
  }
  
  /*An array containing all the country names in the world:*/
  var gameList = ["Minecraft","Grand Theft Auto V","Tetris (EA-Version)","Wii Sports","PUBG: Battlegrounds","Mario Kart 8 (Deluxe)","Overwatch","Tetris (Nintendo-Version)","Red Dead Redemption 2","Super Mario Bros.","Counter-Strike: Global Offensive","Animal Crossing: New Horizons","Mario Kart Wii","Terraria","Wii Sports Resort","Pokémon Rote und Blaue Edition","New Super Mario Bros.","New Super Mario Bros. Wii","The Elder Scrolls V: Skyrim","Grand Theft Auto: San Andreas","The Witcher 3: Wild Hunt","Diablo III","Call of Duty: Modern Warfare","Human: Fall Flat","Duck Hunt","Wii Play","Super Smash Bros. Ultimate","Call of Duty: Modern Warfare 3","Call of Duty: Black Ops","Borderlands 2","The Legend of Zelda: Breath of the Wild","Grand Theft Auto IV","Grand Theft Auto: Vice City","Grand Theft Auto III","Call of Duty: Black Ops II","FIFA 18","Kinect Adventures!","Nintendogs","Pokémon Schwert und Schild","Mario Kart DS","Pokémon Goldene und Silberne Edition","Super Mario Odyssey","Call of Duty: Modern Warfare 2","Wii Fit","Wii Fit Plus","Super Mario World","Frogger","Lemmings","Marvel’s Spider-Man","The Last of Us","FIFA 19","Garry’s Mod","Dr. Kawashimas Gehirn-Jogging","Call of Duty: Ghosts","Mario Kart 7","Super Mario Land","Monster Hunter: World","Pokémon Diamant- und Perl-Edition","Super Mario Party","Super Mario Bros. 3","Sonic & Sega All-Stars Racing","Pokémon X und Y","Pokémon Sonne und Mond","Pokémon Rubin- und Saphir-Edition","Die Sims","Need for Speed: Most Wanted","Uncharted 4: A Thief’s End","FIFA 11","FIFA 16","Call of Duty 4: Modern Warfare","Call of Duty: World at War","Pokémon Schwarze und Weiße Edition","Red Dead Redemption","Battlefield 3","Need for Speed: Underground","Sonic the Hedgehog","Stardew Valley","Borderlands 3"];
  
  /*initiate the autocomplete function on the "form.name" element, and pass along all games as an array as possible autocomplete values:*/
  autocomplete(document.getElementById("gameName").firstElementChild, gameList);

 