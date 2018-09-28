import { Component } from '@angular/core';
import { Http, Response, RequestOptions, Headers, URLSearchParams} from '@angular/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'Frontend Test Application';

  // If you like to access a variable in your html, assign it first here.
  response: String;

  apiRoot: String = 'http://httpbin.org';

  constructor(private http: Http) { }

  doGET(search_value) {
    console.log("GET");
    let url = `${this.apiRoot}/get`;
    let search = new URLSearchParams();
    search.set('username', search_value);
    search.set('limit', '25');
    this.http.get(url, {search}).subscribe(
        res => {
          this.response = JSON.parse(res._body);
          console.log(this.response);
        },
        error => console.log(error)
      );
  }

  getUsername(username) {
    let url = 'http://127.0.0.1:5000/user/' + username;
    this.http.get(url).subscribe(
      res => {
        this.response = JSON.parse(res._body);
        console.log(this.response);
      },
      error => console.log(error)
    );
  }

}
