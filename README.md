# Instruction
You must send files using multipart/form-data to the address
`http://host:port/`

File with config must have field is `config`

# The structure of the configuration file
| Name | Type | Description |
| --- | --- | --- |
| key | string | Secret key. It's installed through the env |
| files | array | Fiels and fields which need to change |

### The field `fields` contains an array of elements
| Name | Type | Description | 
| --- | --- | --- |
| filename | string | Pdf file name |
| fields | array | Key and value for pdf file |

### The fields of `fields`
| Name | Type | Description | 
| --- | --- | --- |
| key | string | Name field (It's set in pdf field) |
| value | string | Value field |


Example file in directory `examples`
