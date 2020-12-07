package helloworld;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;
import com.amazonaws.services.lambda.runtime.events.APIGatewayProxyRequestEvent;
import com.amazonaws.services.lambda.runtime.events.APIGatewayProxyResponseEvent;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import software.amazon.awssdk.auth.credentials.EnvironmentVariableCredentialsProvider;
import software.amazon.awssdk.http.SdkHttpClient;
import software.amazon.awssdk.http.urlconnection.UrlConnectionHttpClient;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.dynamodb.DynamoDbClient;

public class ApiGatewayHandler implements RequestHandler<APIGatewayProxyRequestEvent, APIGatewayProxyResponseEvent> {
    private static Gson gson = new GsonBuilder().setPrettyPrinting().create();
    private static SdkHttpClient sdkHttpClient = UrlConnectionHttpClient.create();
    private static DynamoDbClient client = DynamoDbClient.builder()
            .httpClient(sdkHttpClient)
            .region(Region.US_EAST_1)
            .credentialsProvider(EnvironmentVariableCredentialsProvider.create())
            .build();
    private static UserRepository userRepository = new DynamoDBUserRepository(client, gson);

    static {
        //Dynamodb warmup
        // it improves performance a lot, because on startup(static initialization) AWS Lambda has CPU Burst
        userRepository.get("invalidId");
    }

    @Override
    public APIGatewayProxyResponseEvent handleRequest(APIGatewayProxyRequestEvent event, Context context) {
        switch (event.getHttpMethod()) {
            case "POST":
                return handleAdd(event);
            case "GET":
                return handleGet(event);
            case "DELETE":
                return handleDelete(event);
            default:
                throw new UnsupportedOperationException("Unsupported http method " + event.getHttpMethod());
        }
    }

    private APIGatewayProxyResponseEvent handleGet(APIGatewayProxyRequestEvent event) {
        APIGatewayProxyResponseEvent responseEvent = new APIGatewayProxyResponseEvent();
        String id = event.getQueryStringParameters().get("id");
        if (id != null) {
            User user = userRepository.get(id);
            if (user != null) {
                responseEvent.setBody(gson.toJson(user));
                responseEvent.setStatusCode(200);
            } else {
                responseEvent.setStatusCode(404);
            }
        } else {
            responseEvent.setStatusCode(404);
        }
        return responseEvent;
    }

    /*
    private APIGatewayProxyResponseEvent handleAdd(APIGatewayProxyRequestEvent event) {
        APIGatewayProxyResponseEvent responseEvent = new APIGatewayProxyResponseEvent();
        User user = gson.fromJson(event.getBody(), User.class);
        userRepository.save(user);
        responseEvent.setStatusCode(201);
        responseEvent.setBody(gson.toJson(user));
        return responseEvent;
    }*/
    
    private APIGatewayProxyResponseEvent handleAdd(APIGatewayProxyRequestEvent event) {
        APIGatewayProxyResponseEvent responseEvent = new APIGatewayProxyResponseEvent();
        System.out.println(event.getBody());
        User user = gson.fromJson(event.getBody(), User.class);
        userRepository.save(user);
        responseEvent.setStatusCode(201);
        responseEvent.setBody(gson.toJson(user));
        return responseEvent;
    }


    private APIGatewayProxyResponseEvent handleDelete(APIGatewayProxyRequestEvent event) {
        APIGatewayProxyResponseEvent responseEvent = new APIGatewayProxyResponseEvent();
        String id = event.getQueryStringParameters().get("id");
        if (id != null) {
            boolean deleted = userRepository.delete(id);
            if (deleted) {
                responseEvent.setStatusCode(200);
            } else {
                responseEvent.setStatusCode(404);
            }
        } else {
            responseEvent.setStatusCode(404);
        }
        return responseEvent;
    }
}
