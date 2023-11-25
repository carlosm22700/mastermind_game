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

## Challenges and Scalability

Throughout the development of this Mastermind game, I encountered several challenges that pushed me to make thoughtful decisions regarding the architecture and tech stack. Here are some key challenges and how I addressed them:

- **Overengineering Prevention**: Initially, the temptation to over-engineer the solution was strong. I contemplated adding more layers of complexity, such as a front-end framework or additional features beyond the scope. However, staying focused on the project's requirements, I scaled back to ensure optimal performance and maintainability.

- **Front-End Simplification**: I considered implementing more intricate client-side rendering and interaction. However, to stay aligned with the backend-focused nature of the project, I decided to leverage Django's templating system. This approach streamlined the development process and kept the focus on server-side logic.

- **Tech Stack Scalability**: The choice of Python with Django, Django-Redis for caching, and PostgreSQL for persistent data storage was deliberate. This combination not only provided the robustness needed for the current application but also laid a foundation for future enhancements. It allows the project to scale efficiently and incorporate additional features like multiplayer modes, API integrations, and more complex game mechanics.

- **Future Growth**: The architecture and technologies used in this project are not only industry-standard but also flexible enough to accommodate future developments. Whether it's integrating a front-end framework, expanding the backend logic, or adding new features, the current setup provides a solid and scalable foundation.

In conclusion, the Mastermind game, as developed, serves as a testament to agile development and scalability. The project, while fulfilling its current objectives, is structured in a way that invites further expansion and complexity, demonstrating the potential for continued growth and evolution.


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

To set up a development environment and contribute to Mastermind:

1. Install Redis following instructions from the [Redis official website](https://redis.io/download).
2. Fork the repo and clone it locally.
3. Install dependencies:
   - Ensure you have Pipenv installed. If not, install it using `pip install pipenv`.
   - Run `pipenv install` to install dependencies from the `Pipfile`.
   - If you prefer using `requirements.txt`, run `pip install -r requirements.txt`.
4. Activate the virtual environment with `pipenv shell`.
5. Start the Django server with `python manage.py runserver`.
6. In a separate terminal, run `redis-server`.

For contributing:

1. Create your feature branch (`git checkout -b feature/amazing-feature`).
2. Commit your changes (`git commit -m 'Add some amazing feature'`).
3. Push to the branch (`git push origin feature/amazing-feature`).
4. Open a Pull Request.

Please adhere to the project's coding standards and include tests where applicable.

## Icebox Features

- **Multiplayer Mode**: Options for players to guess a combination set by their opponent.
- **API for Leaderboards**: An API to fetch high scores and game data for competitive play.
- **Difficulty Modes**: Additional modes, including a Wordle-style variant with string guesses.

*Note: These features are prospective and not currently implemented.*

## Deployment

The app is deployed on Heroku. To replicate the deployment process or run your own instance, refer to the deployment guide at the start of this document.

---

Remember to replace the Heroku link with your actual app's URL and adjust any sections as necessary to fit your project's specifics.
