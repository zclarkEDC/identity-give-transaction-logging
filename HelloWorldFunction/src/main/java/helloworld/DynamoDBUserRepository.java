package helloworld;

import com.google.gson.Gson;
import lombok.extern.slf4j.Slf4j;
import software.amazon.awssdk.services.dynamodb.DynamoDbClient;
import software.amazon.awssdk.services.dynamodb.model.AttributeValue;
import software.amazon.awssdk.services.dynamodb.model.ConditionalCheckFailedException;
import software.amazon.awssdk.services.dynamodb.model.DeleteItemRequest;
import software.amazon.awssdk.services.dynamodb.model.GetItemRequest;
import software.amazon.awssdk.services.dynamodb.model.PutItemRequest;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;

@Slf4j
public class DynamoDBUserRepository implements UserRepository {
    public static final String TABLE = "users";
    private static final String ID = "id";
    private static final String USER = "user";
    private final DynamoDbClient client;
    private final Gson gson;

    public DynamoDBUserRepository(DynamoDbClient client, Gson gson) {
        this.client = client;
        this.gson = gson;
    }

    @Override
    public User get(String userId) {
        Map<String, AttributeValue> keyMap = new HashMap();
        keyMap.put(ID, AttributeValue.builder().s(userId).build());
        Map<String, AttributeValue> item = client.getItem(GetItemRequest.builder()
                .tableName(TABLE)
                .key(keyMap)
                .build()).item();
        return Optional.ofNullable(item)
                .filter(x -> x.containsKey(USER))
                .map(this::buildUserFromItem)
                .orElse(null);
    }

    private User buildUserFromItem(Map<String, AttributeValue> item) {
        return gson.fromJson(item.get(USER).s(), User.class);
    }

    @Override
    public User save(User user) {
        if (user.getId() == null) {
            user.setId(UUID.randomUUID().toString());
        }
        Map<String, AttributeValue> userAsMap = new HashMap<>();
        /*
        Map<String,String> values = new HashMap<>();
        values.put(USER, AttributeValue.builder().s(gson.toJson(user)).build());


        Map<String,String> temp = new HashMap<>();
        for (Entry<String,String> entry : values.entrySet()) {
        if ("some value".equals(entry.getValue())) {
        temp.put(entry.getValue(), "another value");
        }
        }
        values.putAll(temp);
*/
        
        userAsMap.put(ID, AttributeValue.builder().s(user.getId()).build());
        userAsMap.put(USER, AttributeValue.builder().s(gson.toJson(user)).build());
        userAsMap.put("tester", AttributeValue.builder().s(gson.toJson(user)).build());
        userAsMap.putAll(AttributeValue.builder().s(gson.toJson(user)).build());
        
        client.putItem(PutItemRequest.builder()
                .item(userAsMap)
                .tableName(TABLE)
                .build());
        log.info("User with id {} was add to DynamoDB", user.getId());
        return user;
    }
    /*
    @Override
    public User save(User user) {
        if (user.getId() == null) {
            user.setId(UUID.randomUUID().toString());
        }
        Map<String, AttributeValue> userAsMap = new HashMap<>();
        userAsMap.put(ID, AttributeValue.builder().s(user.getId()).build());
        userAsMap.put(USER, AttributeValue.builder().s(gson.toJson(user)).build());
        client.putItem(PutItemRequest.builder()
                .item(userAsMap)
                .tableName(TABLE)
                .build());
        log.info("User with id {} was add to DynamoDB", user.getId());
        return user;
    }*/


    @Override
    public boolean delete(String userId) {
        Map<String, AttributeValue> keyMap = new HashMap();
        keyMap.put(ID, AttributeValue.builder().s(userId).build());
        try {
            client.deleteItem(DeleteItemRequest.builder()
                    .tableName(TABLE)
                    .conditionExpression("attribute_exists(id)")
                    .key(keyMap)
                    .build());
            log.info("User with id {} was deleted from DynamoDB", userId);
        } catch (ConditionalCheckFailedException e) {
            log.warn("User with id {} doesn't exist", userId);
            return false;
        }
        return true;

    }
}
