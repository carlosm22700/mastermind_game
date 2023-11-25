# Mastermind Game

Play the game here: [Mastermind on Heroku](https://mastermind-1124-c25a7a9dfcb2.herokuapp.com/login/)

Check out my Trello board: [Planning on Trello](https://trello.com/b/lle8pjV4/mastermindplanning)

## How to Play

Visit the live deployment link above and follow these steps to play Mastermind:

1. **Sign In or Sign Up**: Create an account or sign in to an existing one.
2. **Start a New Game**: Click 'Start Game' to generate a random winning combination.
3. **Make Your Guess**: Enter your guess of four numbers (0-7) within 5 minutes.
4. **Check the Results**: After each guess, the game evaluates your input.
5. **Game Over Conditions**: Failing to guess the combination within 10 attempts or letting the timer run out results in a game over.
6. **Winning**: Correctly guessing the combination wins the game!

## Technologies Used

- **Python & Django**: Robust and readable, Python paired with Django offers a mature stack with a strong community and comprehensive libraries.
- **Django-Redis**: For efficient caching, enabling fast retrieval of the game's state without hitting the database frequently.
- **PostgreSQL**: A powerful, open-source object-relational database system used for persistent data storage.
- **Random.org API**: To ensure true randomness in the game's number generation, providing a fair and unpredictable challenge.
- **Heroku**: A cloud platform as a service enabling scalable deployments.
- **Gunicorn**: A Python WSGI HTTP server for UNIX, serving Python applications across the web.

## Architecture and Code Configuration

The application follows the Model-View-Template (MVT) architecture, which is Django's take on the classic Model-View-Controller (MVC) pattern. Here's how the components are structured:

- **Models**: Define the data structures and are used to interact with the database.
- **Views**: Contain the logic to process HTTP requests and return HTTP responses.
- **Templates**: Handle the presentation layer, displaying information and interfaces to the user.
- **Game Logic**: Encapsulated in `game_class.py`, containing all game-related operations and states.
- **User Interaction**: Managed through Django's forms and sessions, allowing for a seamless and secure user experience.

This structure provides a clear separation of concerns, making the codebase manageable and scalable.

## Contributing

To contribute to Mastermind:

1. Fork the repo and clone it locally.
2. Create your feature branch (`git checkout -b feature/amazing-feature`).
3. Commit your changes (`git commit -m 'Add some amazing feature'`).
4. Push to the branch (`git push origin feature/amazing-feature`).
5. Open a Pull Request.

Please ensure your contributions adhere to the project's coding standards and include tests where applicable.

## Icebox Features

- **Multiplayer Mode**: Options for players to guess a combination set by their opponent.
- **API for Leaderboards**: An API to fetch high scores and game data for competitive play.
- **Difficulty Modes**: Additional modes, including a Wordle-style variant with string guesses.

*Note: These features are prospective and not currently implemented.*

## Deployment

The app is deployed on Heroku. To replicate the deployment process or run your own instance, refer to the deployment guide at the start of this document.

---

Remember to replace the Heroku link with your actual app's URL and adjust any sections as necessary to fit your project's specifics.
