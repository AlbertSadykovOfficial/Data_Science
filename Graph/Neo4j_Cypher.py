"""

		Neo4j -> Язык запросов Cypher
	
			БД Neo4j имет в своем распоряжении язык запросов Cypher, которым удобно работмать с графовыми данными:
				http://neo4j.com/docs/stable/cypher-query-lang.html

			Cypher + Python:
				http://neo4j.com/developer/python/


			Пример поиска на языке Cypher (Кого знает Илья?):

				Match(u1:User { name: 'Ilya' })-[:knows]->(u2:User)
				Return u2.name

			Пример создания данных на языке Cypher:
			
				CREATE (user1:User {name: 'Annelies'}),
				(user2:User {name: 'Paul', LastName: 'Ragnar'}),
				(user2:User {name: 'Mahuba'}),
				(country1:Country {name: 'Mongolia'}),
				(country2:Country {name: 'Sweden'}),
				(food1:Food {name: 'Sushi'}),
				(hobby1:Hobby {name: 'Trevelling'}),
				(user1)-[:Has_been_in]->(country1),
				(user1)-[:Has_been_in]->(country2),
				(user2)-[:Has_been_in]->(country1),
				(user1)-[:Is_mother_of]->(user2),
				(user2)-[:knows]->(user3),
				(user3)-[:Likes]->(food1),
				(user1)-[:Is_born_in]->(county1),

			Пример - Создать новый узел и оношение:
				Merge (user3)-[:Loves]->(hobby1)

			Пример (вернуть все узлы и отношения)

				Math (n)-[r]-()
				Return n,r
			
			Пример - В каких странах была Аннелиз:

				Match (u:User {name: 'Annelis'})-(:Has_been_in)->(c:Country)
				Return u.name, c.name

			Пример - кто в какой стране побывал

				Match ()-[r:Has_been_in]->()
				Return r LIMIT 25

			Удалить все узлы и отношения в БД:

				MATCH(n)
				Optional MATCH (n)-[r]-()
				Delete n,r

"""