parsing_prompt = """
You will be given the contents of a PDF. Your job is to parse it and return the github username of a prominent tech company mentioned in there.

Your output should strictly follow the following format (replace 'xyz' placeholders with the actual answers) if only 1 company is mentioned: 

@@@json
{
	"num_companies": "1",
	"github_username_1": "xyz",
}
@@@


If there are more than one companies mentioned in the contents, then output in the following format: (replace the 'xyz' and 'n' placeholders with the actual values)

@@@json
{
	"num_companies": "n",
	"github_username_1": "xyz",
	"github_username_2": "xyz",
	...
	"github_username_n": "xyz",
}
@@@

Make sure your output exactly follows the structure mentioned above, including the '@@@' suffix and prefix. Make sure all the fields are double quotes and not single quotes.
"""