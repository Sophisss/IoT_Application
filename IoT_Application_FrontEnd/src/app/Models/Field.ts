export class Field {

    name : String 
    type : String
    required : Boolean
    minLenght : Number | undefined  
    maxLength: Number | undefined
    minimum: Number | undefined
    maximum : Number | undefined
    allowed_values : String[] = [] 

    constructor(name : String, type: String, required: Boolean){
        this.name = name
        this.type = type
        this.required = required
    }

    setMinLength(minLenght: Number): void {
        this.minLenght =  minLenght;
    }

    setMaxLength(maxLength: Number): void {
        this.maxLength =  maxLength;
    }

    setMinimum(minimum: Number): void {
        this.minimum =  minimum;
    }

    setMaximum(maximum: Number): void {
        this.maximum =  maximum;
    }
}