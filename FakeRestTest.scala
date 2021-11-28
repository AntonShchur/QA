import scala.concurrent.duration.*
import io.gatling.core.Predef.*
import io.gatling.http.Predef.*

import scala.util.Random

object RandomDataGenerator {
  val alpha = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
  def randomString(length: Int) = scala.util.Random.alphanumeric.take(length).mkString

  def randomInt(): Int ={
    val random = new Random().nextInt(100)
    random
  }

  def randomBook() : String =
    """{"id":"""".stripMargin + RandomDataGenerator.randomInt() + """",
      |"title":"""".stripMargin + RandomDataGenerator.randomString(25) + """",
      |"description":"""".stripMargin + RandomDataGenerator.randomString(25) + """",
      |"pageCount":"""".stripMargin + RandomDataGenerator.randomInt() + """",
      |"excerpt":"""".stripMargin + RandomDataGenerator.randomString(25) + """",
      |"publishDate":"2021-11-27T14:03:17.287Z"}""".stripMargin
}

class FakeApiSimulation extends Simulation {

  val httpProtocol = http.baseUrl("https://fakerestapi.azurewebsites.net")

  val getBookbyId = scenario("Get Book by Id")
        .exec(sessionPostBook => {
          val sessionPostUpdate = sessionPostBook.set("postrequest", RandomDataGenerator.randomBook())
          sessionPostUpdate
        })
        .exec(
          http("Post Book")
            .post("/api/v1/Books")
            .body(StringBody("${postrequest}")).asJson
            .check(jsonPath("$.id").saveAs("bookId"))
        )
        .exitHereIfFailed
    .exec(
      http("Get Books")
        .get("/api/v1/Books/${bookId}")
    )

  val getAllBooks = scenario("Get Books")
    .exec(
      http("Get Books")
        .get("/api/v1/Books")
    )


  val postBook = scenario("Post Books")
      .exec(sessionPostBook => {
        val sessionPostUpdate = sessionPostBook.set("postrequest", RandomDataGenerator.randomBook())
        sessionPostUpdate
      }).exec(http("Post Books")
          .post("/api/v1/Books")
          .body(StringBody("${postrequest}")).asJson)

  val putBook = scenario("Put Books")
    .exec(sessionPostBook =>
    {val CreateBook = sessionPostBook.set("postrequest", RandomDataGenerator.randomBook())
      CreateBook
    })
    .exec(http("Put Books")
      .post("/api/v1/Books")
      .body(StringBody("${postrequest}")).asJson
      .check(jsonPath("$.id").saveAs("bookId"))
    )
    .exitHereIfFailed
    .exec(sessionPutBook =>
    {
      val UpdateBook = sessionPutBook.set("putrequest", RandomDataGenerator.randomBook())
      UpdateBook
    })
    .exec(http("Put Book").put("/api/v1/Books/${bookId}").body(StringBody("${putrequest}")).asJson)

  val deleteBook = scenario("Delete Books")
    .exec(sessionPostBook =>
    {val CreateBook = sessionPostBook.set("postrequest", RandomDataGenerator.randomBook())
      CreateBook
    })
    .exec(http("Put Books")
      .post("/api/v1/Books")
      .body(StringBody("${postrequest}")).asJson
      .check(jsonPath("$.id").saveAs("bookId"))
    )
    .exitHereIfFailed
    .exec(http("Delete Books").delete("/api/v1/Books/${bookId}"))

  setUp(getAllBooks.inject(rampUsers(5).during(10.seconds)).protocols(httpProtocol),
        getBookbyId.inject(rampUsers(5).during(10.seconds)).protocols(httpProtocol),
        deleteBook.inject(rampUsers(5).during(10.seconds)).protocols(httpProtocol),
        putBook.inject(rampUsers(5).during(10.seconds)).protocols(httpProtocol),
        postBook.inject(rampUsers(5).during(10.seconds)).protocols(httpProtocol))
}
