import java.net.URI;
import java.net.http.*;
import java.net.http.HttpResponse.BodyHandlers;

public class PKIClient {
    private static final String BASE = "http://localhost:5000/api/v1";
    private final HttpClient client = HttpClient.newHttpClient();

    public String issueCert(String commonName) throws Exception {
        String body = "{\"common_name\":\"" + commonName + "\"}";
        HttpRequest req = HttpRequest.newBuilder()
            .uri(URI.create(BASE + "/issue"))
            .header("Content-Type", "application/json")
            .POST(HttpRequest.BodyPublishers.ofString(body))
            .build();
        return client.send(req, BodyHandlers.ofString()).body();
    }

    public String getCertStatus(String commonName) throws Exception {
        HttpRequest req = HttpRequest.newBuilder()
            .uri(URI.create(BASE + "/status/" + commonName))
            .GET().build();
        return client.send(req, BodyHandlers.ofString()).body();
    }

    public String revokeCert(String commonName) throws Exception {
        String body = "{\"common_name\":\"" + commonName + "\"}";
        HttpRequest req = HttpRequest.newBuilder()
            .uri(URI.create(BASE + "/revoke"))
            .header("Content-Type", "application/json")
            .POST(HttpRequest.BodyPublishers.ofString(body))
            .build();
        return client.send(req, BodyHandlers.ofString()).body();
    }

    public static void main(String[] args) throws Exception {
        PKIClient pki = new PKIClient();
        System.out.println("Issuing cert...");
        System.out.println(pki.issueCert("test.harshita.com"));
        System.out.println("Status check...");
        System.out.println(pki.getCertStatus("test.harshita.com"));
    }
}