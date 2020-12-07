package helloworld;

public interface UserRepository {
    User get(String userId);

    User save(User user);

    boolean delete(String user);
}
