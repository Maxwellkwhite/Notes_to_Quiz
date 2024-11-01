import os
from openai import OpenAI
import json

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
                {"role": "system", "content": "You are a quiz generator assistant."},
                {
                    "role": "user",
                    "content": f"""Create a quiz based on the following notes. Ignore any pictures or links. Output the quiz in JSON format and only output the JSON. Do it with the following structure:
                    {{
                        "title": "Quiz Title",
                        "questions": [
                            {{
                                "question": "Question text",
                                "options": ["Option A", "Option B", "Option C", "Option D"],
                                "correct_answer": "Correct option",
                                "explanation": "Explanation for the correct answer"
                            }},
                            // More questions...
                        ]
                    }}
                    
                    Don't include the letter in the option choices or correct answer. Make the quiz a suitable length based on the notes provided. Here are the notes to base the quiz on:
                    1 Supply and demand
1.1 Lecture 2: Supply and Demand
1.1.1 Supply and demand diagrams:
• Demand Curve measures willingness of consumers to buy the good
• Supply Curve measures willingness of producers to sell
• Intersection of supply and demand curve is market equilibrium.
• Supply and demand curves can shift when there are
– shocks to the ability of producers to supply
– shocks in consumer tastes
– shocks to the price of complement/substitute goods. A rise in the
price of a substitute good for good X raises the demand for the X.
• Interventions in market can lead to disequilibrium:
– for example, imposing a minimum wage means that more people will
want to work than employers want to hire at the minimum wage.
This creates unemployment.
• The cost of these interventions is found in reduced eÿciency (trades that
are not made); there may be benefts in greater equity.
1.1.2 TO KNOW- Conceptual Understanding
• Explain the di˙erence between a movement along the demand (supply)
curve and a shift of the demand (supply) curve
• Describe factors that shift supply and demand curves
• Know “what’s wrong” with excess supply or excess demand
1.1.3 TO KNOW- Graphical and Math Understanding
• Find a market equilibrium given a demand and supply curve- (a) graphi-
cally and (b) using algebraic expressions
• Analyze the e˙ect of a price ceiling in a graph
• Analyze the e˙ect of a price foor in a graph
1
1.2 Lecture 3: Applying supply and demand
1.2.1 Elasticity
• Price elasticity of demand is defned
∂Q
 = Q
∂P
P
• Perfectly inelastic demand is  = 0 and perfectly elastic demand
is  = −∞.
• The elasticity a˙ects consumers’ response to a shift in price: if the elas-
ticity is between 0 and -1, then frms can raise revenues by raising the
price (since consumers will still buy the good in signifcant quantities); if
 < −1, then raising the price results in a decline in frm revenue.
• Accurately estimating an elasticity requires a shift along the supply curve
(e.g., a tax on suppliers).
• Perfectly inelastic demand is characteristic of a good with no substitutes;
perfectly elastic demand is a good with perfect substitutes
1.2.2 TO KNOW- Conceptual Understanding
• Explain what the elasticity of demand/supply imply about changes in
equilibria.
1.2.3 TO KNOW- Graphical and Math Understanding
• Given an algebraic expression for demand, calculate the price elasticity of
demand at any point along the curve
• Given an algebraic expression for supply, calculate the price elasticity of
supply at any point along the curve
• Analyze the e˙ect of a specifc tax in a graph
• Analyze the e˙ect of a specifc tax using algebra
2 Consumer Theory
2.1 Lecture 4: Preferences and utility
2.1.1 Preferences
• We impose three assumptions about consumer preferences: preferences
are complete, transitive and non-satiated.
• These yield four assumptions about utility curves:
2
– consumers prefer higher indi˙erence curves,
– they are downward-sloping,
– they never cross
– there is one indi˙erence curve through every consumption bundle.
2.1.2 Utility
• Utility function is a function that transfers bundles of goods into a scale
of utils; however, it provides only an ordinal ranking, not a cardinal one.
• A general assumption employed is diminishing marginal utility: consumers
receive less utility from each unit of a good they consume.
• The slop of the indi˙erence curve is called the marginal rate of substi-
tution
– MRS is the ratio of marginal utilities;
∂U
= − M Ux ∂X
M RS = −M UY ∂U
∂Y
– diminishing as you move along the indi˙erence curve.
2.1.3 TO KNOW- Graphical and Math Understanding
• Prove that indi˙erence curves never cross using a fgure
• Prove that indi˙erence curves are downward sloping using a fgure
• Explain why consumers prefer high indi˙erence curves using a fgure
• Draw indi˙erence curves corresponding to perfect complements and per-
fect substitutes
• Know how to sketch an indi˙erence curve given a verbal description of a
consumer’s preferences
• Calculate marginal utilities given a utility function
• Calculate marginal rate of substitution given a utility function
2.2 Lecture 5: Budget constraints and constrained choice
2.2.1 Budget Constraint
• Budget constraint over two goods X and Y is defned
I = pX X + pY Y.
3
• Slope of the budget constraint is defned as marginal rate of transfor-
mation: rate at which you can transform one good into the other in the
marketplace.
= − pX
M RT pY
• Shifts in price and income alter the position and slope of the budget con-
straint.
2.2.2 Constrainted Optimization
• The optimal bundle that a consumer can choose is defned by the point of
tangency between the indi˙erence curve and the budget line:
∂U
= − M Ux ∂X
M RS = − = M RT∂U = − pX
M UY pY∂Y
• This is equivalent to equating the marginal cost and beneft of consuming
each good.
• The above equation defnes an interior solution (in which the consumer
consumes some of each good); if indi˙erence curves are fat, there can also
be corner solutions in which the consumer only consumes one good.
2.2.3 TO KNOW- Graphical and Math Understanding
• Know how to write down a budget constraint given prices and income
• Show graphically how to fnd the bundle that maximizes the consumer’s
utility subject to the budget constraint
• Solve for the optimal bundle mathematically for a consumer given a utility
function, prices of the two goods, and income; be sure to check for corner
solutions
2.3 Lecture 6: Deriving demand curves
• We can use the constrained optimization problem to derive the demand
curve. In other words, as we change prices of goods, we can observe
how quantities demanded for those goods change, thereby tracing out the
demand curve (the relationship between quantity and price demanded)
2.3.1 Changes in income
• As you change income, you can trace out the relationship between income
and consumption- the Engel Curve
• This also allows us to defne the income elasticity of demand:
∂Q
γ = Q
∂Y
Y
4
• Normal goods- the income elasticity is positive, so as income rises, you
consume the same or more of these goods
• Inferior goods- consumption declines when income increases
• Necessities are goods with γ < 1 - goods where you spend a smaller
share of your income on them as income goes up - like food
– Not saying that you buy less food as income rises - only that you
spend a smaller fraction of your income on food as income rises
• Luxuries are goods with γ > 1 - goods where you spend a larger share
of your income on them as income rises - like cars, jewelry
2.3.2 Changes in prices
• An increase in price, has two e˙ects:
– it makes the consumer relatively poorer (income e˙ect)
– and it also makes this specifc good less attractive relative to alter-
natives (substitution e˙ect).
• The substitution e˙ect can be interpreted as the shift in goods consumed
from the original point to the optimal point for a budget constraint that
has the new slope, but is tangent to the old indi˙erence curve.
• Substitution e˙ect is always negative, but income e˙ect can be positive.
• Accordingly, the overall e˙ect of a price increase on consumption of a good
can be negative (for a normal good) or positive, if the good is inferior
and the income e˙ect is larger than the substitution e˙ect.
• A good with a positive own-price elasticity is known as a Gi˙en good.
5
2.3.3 TO KNOW- Conceptual Understanding
• Explain what quantities observed after price changes imply about the
income and subsitution e˙ects
2.3.4 TO KNOW- Graphical and Math Understanding
• Graph budget constraint lines and show how the line shifts or rotates when
a price of a good changes or the agent’s income changes
• Derive a demand curve mathematically given a utility function, the price
of one of the goods, and an income level
• Derive an Engel curve mathematically given a utility function and the
price of both goods
• Show and calculate the e˙ect of a price change in a graph showing a con-
sumer’s optimal bundle; decompose the e˙ect graphically into the income
and substitution e˙ect
6
2.4 Lecture 7: Income / substitution e˙ects and labor
supply
• Income and substitution e˙ects can be used to analyze labor supply:
– leisure (time not spent working) is a consumption good
– the price of that good is the wage, since that is the opportunity cost
of time not spent working.
– When the wage rate increases, this also has both an income e˙ect
and a substitution e˙ect.
∗ Income e˙ect: each worker is now richer, and may want to work
less (consume more leisure).
∗ Substitution e˙ect: returns to working are higher, each worker
may want to work more.
∗ If the income e˙ect more than o˙sets the substitution e˙ect,
labor supply may go down when income increases.
2.4.1 TO KNOW- Graphical and Math Understanding
• Calculate the income and substition e˙ects due to changes in wages
• Show the e˙ect of a change in wage in a graph of the labor supply decision;
decompose the e˙ect graphically into the income and substitution e˙ect
7
MIT OpenCourseWare
https://ocw.mit.edu
14.01 Principles of Microeconomics
Fall 2018
For information about citing these materials or our Terms of Use, visit: https://ocw.mit.edu/terms."""
                }
    ]
)

quiz_json = completion.choices[0].message.content
quiz_json = quiz_json.replace("```json\n", "")
quiz_json = quiz_json.replace("```", "")
# Add these debug lines before the json.loads()
print("quiz_json content:", quiz_json)
print("quiz_json type:", type(quiz_json))

# First, ensure your quiz_json string is properly formatted without truncation
# Clean up the JSON string by removing duplicated/truncated lines

# Then parse it
quiz_data = json.loads(quiz_json)
# Save quiz to JSON file with proper formatting
with open('economics_quiz.json', 'w') as f:
    json.dump(quiz_data, f, indent=4)
