from orm_choices import choices

# choice for available user types
@choices
class UserTypes:
	class Meta:
		LIBRARIAN = [0, "Librarian"]
		AUTHOR = [1, "Author"]
		PUBLISHER = [2, "Publisher"]
		OTHER = [3, "Other"]

# choice for gender
@choices
class Gender:
	class Meta:
		OTHER = [0, "Other"]
		MALE = [1, "Male"]
		FEMALE = [2, "Female"]
		UNKNOWN = [3, "Unknown"]