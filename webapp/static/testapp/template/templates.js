'use strict';

define(
  function() {
    var indexItem = 
    '<table class="table">\
      <thead>\
        <tr>\
          <th> title </th>\
          <th> source </th>\
          <th> date </th>\
        </tr>\
      </thead>\
      <tbody>\
        <% for(var i = 0; i < items.length; i++){ %>\
         <% var item = items[i]; %>\
            <tr>\
                 <td> <a href="/get/<%= item.url%>"><%= item.title %></a></td>\
                 <td><%= item.source %></td>\
                 <td><%= item.date %></td>\
            </tr>\
        <% } %>\
      </tbody>\
     </table>';

    return {
      indexItem: indexItem,
    }
  }

);
