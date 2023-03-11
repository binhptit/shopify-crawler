# curl -X POST "https://partners.shopify.com/1095746/api/2023-01/graphql.json" \
#   -H "Content-Type: application/graphql" \
#   -H "X-Shopify-Access-Token: prtapi_02c831dced84b41b8eea11c947112524" \
#   -d '
#     {
#       conversations(
#         first: 20,
#         unreadOnly: true,
#         statuses: [ACTIVE],
#       ) {
#         edges {
#           node {
#             id
#             merchantUser {
#               name
#             }
#           }
#         }
#       }
#     }
#     '

# <!-- createdAtMax: "2023-02-15T20:47:55.123456Z" -->

# (before: "eyJwYXJ0bmVyX3JlY2VpdmFibGVfY3JlYXRlZF9hdCI6MTY3ODQzOTU5NDAwMCwiaWQiOiIyMDExOTk2MTYifQ", last: 20)
# (before: "eyJwYXJ0bmVyX3JlY2VpdmFibGVfY3JlYXRlZF9hdCI6MTY3ODQzOTU5NDAwMCwiaWQiOiIyMDExOTk2MTYifQ", last: 10)

# curl -X POST \
#   https://partners.shopify.com/1095746/api/2023-01/graphql.json \
#   -H 'Content-Type: application/graphql' \
#   -H 'X-Shopify-Access-Token: prtapi_02c831dced84b41b8eea11c947112524' \
#   -d '{transactions (last: 20, before : "eyJwYXJ0bmVyX3JlY2VpdmFibGVfY3JlYXRlZF9hdCI6MTY3ODQzOTU5NDAwMCwiaWQiOiIyMDExOTk2MTYifQ") {
#     edges {
#       cursor
#       node {
#         id
#         createdAt
#         ... on AppSubscriptionSale {
#           billingInterval
#           shop {
#             name
#           }
#           app {
#             name
#           }
#           netAmount{
#               amount
#               currencyCode
#           }
#         }
#       }
#     }
#   }}'


# curl -X POST \
#   https://partners.shopify.com/1095746/api/2023-01/graphql.json \
#   -H 'Content-Type: application/graphql' \
#   -H 'X-Shopify-Access-Token: prtapi_02c831dced84b41b8eea11c947112524' \
#   -d '{
#     app (id: "gid://partners/App/5113899") {
#       name
#       events {
#         edges {
#           cursor
#           node {
#             type
#             occurredAt
#             shop {
#               name
#               myshopifyDomain
#             }
#           }
#         }
#       }
#     }
#   }'
